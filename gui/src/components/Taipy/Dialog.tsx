import React, { MouseEvent, ReactNode, useCallback, useContext, useMemo } from "react";
import Button from "@mui/material/Button";
import DialogTitle from "@mui/material/DialogTitle";
import MuiDialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import Tooltip from "@mui/material/Tooltip";
import { Theme } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import { SxProps } from "@mui/system";

import { TaipyContext } from "../../context/taipyContext";
import { createSendActionNameAction } from "../../context/taipyReducers";
import TaipyRendered from "../pages/TaipyRendered";
import { TaipyActiveProps } from "./utils";
import { useDynamicProperty } from "../../utils/hooks";

interface DialogProps extends TaipyActiveProps {
    title: string;
    tp_onAction?: string;
    closeLabel?: string;
    labels?: string;
    page?: string;
    partial?: boolean;
    open?: boolean;
    defaultOpen?: string | boolean;
    children?: ReactNode;
    height?: string | number;
    width?: string | number;
}

const closeSx: SxProps<Theme> = {
    color: (theme: Theme) => theme.palette.grey[500],
    marginTop: "-0.6em",
    marginLeft: "auto",
    alignSelf: "start",
};
const titleSx = { m: 0, p: 2, display: "flex", paddingRight: "0.1em" };

const Dialog = (props: DialogProps) => {
    const {
        id,
        title,
        defaultOpen,
        open,
        tp_onAction = "",
        closeLabel = "Close",
        page,
        partial,
        className,
        width,
        height,
    } = props;
    const { dispatch } = useContext(TaipyContext);

    const active = useDynamicProperty(props.active, props.defaultActive, true);
    const hover = useDynamicProperty(props.hoverText, props.defaultHoverText, undefined);

    const handleAction = useCallback(
        (evt: MouseEvent<HTMLElement>) => {
            const { idx = "-1" } = evt.currentTarget.dataset;
            dispatch(createSendActionNameAction(id, tp_onAction, parseInt(idx, 10)));
        },
        [dispatch, id, tp_onAction]
    );

    const labels = useMemo(() => {
        if (props.labels) {
            try {
                return JSON.parse(props.labels) as string[];
            } catch (e) {
                console.info(`Error parsing dialog.labels\n${(e as Error).message || e}`);
            }
        }
        return [];
    }, [props.labels]);

    const paperProps = useMemo(() => {
        if (width !== undefined || height !== undefined) {
            const res = { sx: {} } as Record<string, Record<string, unknown>>;
            if (width !== undefined) {
                res.sx.width = width;
                res.sx.maxWidth = width;
            }
            if (height !== undefined) {
                res.sx.height = height;
            }
            return res;
        }
        return {};
    }, [width, height]);

    return (
        <MuiDialog
            id={id}
            onClose={handleAction}
            open={open === undefined ? defaultOpen === "true" || defaultOpen === true : !!open}
            className={className}
            PaperProps={paperProps}
        >
            <Tooltip title={hover || ""}>
                <DialogTitle sx={titleSx}>
                    {title}
                    <IconButton aria-label="close" onClick={handleAction} sx={closeSx} title={closeLabel} data-idx="-1">
                        <CloseIcon />
                    </IconButton>
                </DialogTitle>
            </Tooltip>

            <DialogContent dividers>
                {page ? <TaipyRendered path={"/" + page} partial={partial} fromBlock={true} /> : null}
                {props.children}
            </DialogContent>
            {labels.length ? (
                <DialogActions>
                    {labels.map((l, i) => (
                        <Button onClick={handleAction} disabled={!active} key={"label" + i} data-idx={i}>
                            {l}
                        </Button>
                    ))}
                </DialogActions>
            ) : null}
        </MuiDialog>
    );
};

export default Dialog;
