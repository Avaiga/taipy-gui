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

import React, { useEffect } from "react";

import { createDownloadAction, createSendActionNameAction, FileDownloadProps } from "../../context/taipyReducers";
import { useDispatch, useModule } from "../../utils/hooks";
import { runXHR } from "../../utils/downloads";

interface GuiDownloadProps {
    download?: FileDownloadProps;
}

const GuiDownload = ({ download }: GuiDownloadProps) => {
    const { name = "", onAction, content } = download || {};
    const dispatch = useDispatch();
    const module = useModule();

    useEffect(() => {
        if (content) {
            runXHR(undefined, content, name, onAction ? ((e?: ProgressEvent) => dispatch(createSendActionNameAction("Gui.download", module, onAction, name, content, e ? e.type: undefined))) : undefined);
            dispatch(createDownloadAction());
        }
    }, [content, name, dispatch, onAction, module]);

    return <></>;
};

export default GuiDownload;
