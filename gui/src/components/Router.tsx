import React, { useEffect, useReducer, useState, ComponentType } from "react";
import axios from "axios";
import type {} from "@mui/lab/themeAugmentation";
import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import { ThemeProvider } from "@mui/material/styles";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { SnackbarProvider } from "notistack";
import { HelmetProvider } from "react-helmet-async";
import JsxParser from "react-jsx-parser";
import { BrowserRouter } from "react-router-dom";

import { TaipyContext } from "../context/taipyContext";
import {
    createBlockAction,
    createSetLocationsAction,
    initializeWebSocket,
    INITIAL_STATE,
    retreiveBlockUi,
    taipyInitialize,
    taipyReducer,
} from "../context/taipyReducers";
import { JSXReactRouterComponents } from "./Taipy";
import Alert from "./Taipy/Alert";
import UIBlocker from "./Taipy/UIBlocker";
import Navigate from "./Taipy/Navigate";
import Menu from "./Taipy/Menu";
import GuiDownload from "./Taipy/GuiDownload";

interface AxiosRouter {
    router: string;
    locations: Record<string, string>;
    blockUI: boolean;
}

const mainSx = { flexGrow: 1, bgcolor: "background.default"};
const containerSx = { display: "flex" };

const Router = () => {
    const [state, dispatch] = useReducer(taipyReducer, INITIAL_STATE, taipyInitialize);
    const [JSX, setJSX] = useState("");
    const refresh = !!JSX;
    const themeClass = "taipy-" + state.theme.palette.mode;

    useEffect(() => {
        if (refresh) {
            // no need to access the backend again, the routes are static
            return;
        }
        if (!state.isSocketConnected) {
            // initialize only when there is an existing ws connection
            // --> assuring that there is a session data scope on the backend
            return;
        }
        // Fetch Flask Rendered JSX React Router
        axios
            .get<AxiosRouter>("/taipy-init", {params: {client_id:state.id || ""}})
            .then((result) => {
                setJSX(result.data.router);
                dispatch(createSetLocationsAction(result.data.locations));
                result.data.blockUI && dispatch(createBlockAction(retreiveBlockUi()));
            })
            .catch((error) => {
                // Fallback router if there is any error
                setJSX('<Router><Routes><Route path="/*" element={NotFound404} /></Routes></Router>');
                console.log(error);
            });
    }, [refresh, state.isSocketConnected, state.id]);

    useEffect(() => {
        initializeWebSocket(state.socket, dispatch);
    }, [state.socket]);

    return (
        <TaipyContext.Provider value={{ state, dispatch }}>
            <HelmetProvider>
                <ThemeProvider theme={state.theme}>
                    <SnackbarProvider maxSnack={5}>
                        <LocalizationProvider dateAdapter={AdapterDateFns}>
                            <BrowserRouter>
                                <Box style={containerSx} className={themeClass}>
                                    <CssBaseline />
                                    <Menu {...state.menu} />
                                    <Box component="main" sx={mainSx}>
                                        <JsxParser
                                            disableKeyGeneration={true}
                                            components={JSXReactRouterComponents as Record<string, ComponentType>}
                                            jsx={JSX}
                                        />
                                    </Box>
                                </Box>
                                <Alert alert={state.alert} />
                                <UIBlocker block={state.block} />
                                <Navigate to={state.to} />
                                <GuiDownload download={state.download} />
                            </BrowserRouter>
                        </LocalizationProvider>
                    </SnackbarProvider>
                </ThemeProvider>
            </HelmetProvider>
        </TaipyContext.Provider>
    );
};

export default Router;
