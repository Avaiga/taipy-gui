import React, { useContext, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { TaipyContext } from "../../context/taipyContext";

import TaipyRendered from "./TaipyRendered";

interface MainPageProps {
    path: string;
    route?: string;
}

const MainPage = (props: MainPageProps) => {
    const { state } = useContext(TaipyContext);
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        if (props.route && location.pathname == `${state.urlPrefix}/`) {
           navigate(props.route);
        }
    }, [location.pathname, navigate, props.route, state.urlPrefix]);

    return <TaipyRendered path={props.path} />;
};

export default MainPage;
