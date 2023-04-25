/*
 * Copyright 2023 Avaiga Private Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 *
 *        http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 * an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations under the License.
 */

import React, { useEffect, useState, useContext, ComponentType } from "react";
import axios from "axios";
import JsxParser from "react-jsx-parser";
import { useLocation } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { ErrorBoundary } from "react-error-boundary";

import { PageContext, TaipyContext } from "../../context/taipyContext";
import { getRegisteredComponents } from "../Taipy";
import { unregisteredRender, renderError } from "../Taipy/Unregistered";
import { createPartialAction } from "../../context/taipyReducers";
import ErrorFallback from "../../utils/ErrorBoundary";
import { getBaseURL } from "../../utils";

interface TaipyRenderedProps {
    path?: string;
    partial?: boolean;
    fromBlock?: boolean;
}

interface HeadProps {
    tag: string;
    props: Record<string, string>;
    content: string;
}

interface AxiosRenderer {
    jsx: string;
    style: string;
    head: HeadProps[];
    context: string;
}

// set global style the traditional way
const setStyle = (id: string, styleString: string): void => {
    let style = document.getElementById(id);
    if (style && style.tagName !== "STYLE") {
        style = null;
        id = "TaiPy_" + id;
    }
    if (!style && styleString) {
        style = document.createElement("style");
        style.id = id;
        document.head.append(style);
    }
    if (style) {
        style.textContent = styleString;
    }
};

const emptyArray: string[] = [];

interface PageState {
    jsx?: string;
    module?: string;
}

const TaipyRendered = (props: TaipyRenderedProps) => {
    const { partial, fromBlock } = props;
    const location = useLocation();
    const [pageState, setPageState] = useState<PageState>({});
    const [head, setHead] = useState<HeadProps[]>([]);
    const { state, dispatch } = useContext(TaipyContext);

    const path = props.path || (state.locations && state.locations[location.pathname]) || location.pathname;

    useEffect(() => {
        // Fetch JSX Flask Backend Render
        if (partial) {
            dispatch(createPartialAction(path.slice(1), false));
        } else {
            axios
                .get<AxiosRenderer>(`taipy-jsx${path}`, {
                    params: { client_id: state.id || "", v: window.taipyVersion },
                })
                .then((result) => {
                    // set rendered JSX and CSS style from fetch result
                    if (typeof result.data.jsx === "string") {
                        setPageState({module: result.data.context, jsx: result.data.jsx });
                    }
                    if (!fromBlock) {
                        setStyle("Taipy_style", result.data.style || "");
                        Array.isArray(result.data.head) && setHead(result.data.head);
                    }
                })
                .catch((error) =>
                    setPageState({
                        jsx: `<h1>${
                            error.response?.data ||
                            `No data fetched from backend from ${path === "/TaiPy_root_page" ? getBaseURL() : path}`
                        }</h1><br></br>${error}`,
                    })
                );
        }
    }, [path, state.id, dispatch, partial, fromBlock]);

    return (
        <ErrorBoundary FallbackComponent={ErrorFallback}>
            {head.length ? (
                <Helmet>{head.map((v) => React.createElement(v.tag, v.props, v.content))}</Helmet>
            ) : null}
            <PageContext.Provider value={pageState}>
                <JsxParser
                    disableKeyGeneration={true}
                    bindings={state.data}
                    components={getRegisteredComponents() as Record<string, ComponentType>}
                    jsx={pageState.jsx}
                    renderUnrecognized={unregisteredRender}
                    allowUnknownElements={false}
                    renderError={renderError}
                    blacklistedAttrs={emptyArray}
                />
            </PageContext.Provider>
        </ErrorBoundary>
    );
};

export default TaipyRendered;
