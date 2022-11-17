/*
 * Copyright 2022 Avaiga Private Limited
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

import React, { useState, useEffect, useCallback, useContext, useRef, KeyboardEvent } from "react";
import TextField from "@mui/material/TextField";
import Tooltip from "@mui/material/Tooltip";

import { TaipyContext } from "../../context/taipyContext";
import { createSendActionNameAction, createSendUpdateAction } from "../../context/taipyReducers";
import { TaipyInputProps } from "./utils";
import { useDynamicProperty } from "../../utils/hooks";

const AUTHORIZED_KEYS = ["Enter", "Escape", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"];

const getActionKeys = (keys?: string): string[] => {
    const ak = keys
        ? keys
              .split(";")
              .filter((v) => AUTHORIZED_KEYS.includes(v.trim()))
              .map((v) => v.trim())
        : [];
    return ak.length > 0 ? ak : [AUTHORIZED_KEYS[0]];
};

const Input = (props: TaipyInputProps) => {
    const {
        className,
        type,
        id,
        updateVarName,
        propagate = true,
        defaultValue = "",
        onAction: onAction,
        onChange: onChange,
        multiline = false,
        linesShown = 5,
    } = props;
    const [value, setValue] = useState(defaultValue);
    const { dispatch } = useContext(TaipyContext);
    const delayCall = useRef(-1);
    const [actionKeys] = useState(() => (onAction ? getActionKeys(props.actionKeys) : []));

    const changeDelay = typeof props.changeDelay === "number" && props.changeDelay >= 0 ? props.changeDelay : 300;
    const active = useDynamicProperty(props.active, props.defaultActive, true);
    const hover = useDynamicProperty(props.hoverText, props.defaultHoverText, undefined);

    const handleInput = useCallback(
        (e: React.ChangeEvent<HTMLInputElement>) => {
            const val = e.target.value;
            setValue(val);
            if (changeDelay) {
                if (delayCall.current > 0) {
                    clearTimeout(delayCall.current);
                }
                delayCall.current = window.setTimeout(() => {
                    delayCall.current = -1;
                    dispatch(createSendUpdateAction(updateVarName, val, onChange, propagate));
                }, changeDelay);
            } else {
                dispatch(createSendUpdateAction(updateVarName, val, onChange, propagate));
            }
        },
        [updateVarName, dispatch, propagate, onChange, changeDelay]
    );

    const handleAction = useCallback(
        (evt: KeyboardEvent<HTMLDivElement>) => {
            if (onAction && actionKeys.includes(evt.key)) {
                const val = evt.currentTarget.querySelector("input")?.value;
                if (changeDelay && delayCall.current > 0) {
                    clearTimeout(delayCall.current);
                    delayCall.current = -1;
                    dispatch(createSendUpdateAction(updateVarName, val, onChange, propagate));
                }
                dispatch(createSendActionNameAction(id, onAction, evt.key, updateVarName, val));
                evt.preventDefault();
            }
        },
        [actionKeys, updateVarName, onAction, id, dispatch, onChange, changeDelay, propagate]
    );

    useEffect(() => {
        if (props.value !== undefined) {
            setValue(props.value);
        }
    }, [props.value]);

    return (
        <Tooltip title={hover || ""}>
            <TextField
                margin="dense"
                hiddenLabel
                value={value === undefined ? "": value}
                className={className}
                type={type}
                id={id}
                label={props.label}
                onChange={handleInput}
                disabled={!active}
                onKeyDown={onAction ? handleAction : undefined}
                multiline={multiline}
                minRows={linesShown}
            />
        </Tooltip>
    );
};

export default Input;
