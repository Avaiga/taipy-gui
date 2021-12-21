import React, { CSSProperties, useCallback, useContext } from "react";
import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

import { BlockMessage, BLOCK_CLOSE, createBlockAction, createSendActionNameAction } from "../../context/taipyReducers";
import { TaipyContext } from "../../context/taipyContext";

interface UIBlockerProps {
    block?: BlockMessage;
}

const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    minWidth: 400,
    width: "30%",
    bgcolor: "background.paper",
    border: "2px solid #000",
    boxShadow: 24,
    p: 4,
} as unknown as CSSProperties;

const UIBlocker = ({ block }: UIBlockerProps) => {
    const { dispatch } = useContext(TaipyContext);
    const handleClose = useCallback(() => {
        if (block && !block.noCancel) {
            dispatch(createSendActionNameAction("UIBlocker", block.action));
            dispatch(createBlockAction(BLOCK_CLOSE));
        }
    }, [block, dispatch]);

    return block === undefined || block.close ? null : (
        <Modal open>
            <Box sx={style} className="taipy-UIBlocker">
                <Typography variant="h6" component="h2">
                    {block.message}
                </Typography>
                {block.noCancel ? null : <Button onClick={handleClose}>Cancel</Button>}
            </Box>
        </Modal>
    );
};

export default UIBlocker;
