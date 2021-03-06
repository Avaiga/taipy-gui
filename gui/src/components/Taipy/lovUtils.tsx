import React, { CSSProperties, useMemo, MouseEvent } from "react";
import Avatar from "@mui/material/Avatar";
import CardHeader from "@mui/material/CardHeader";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import Tooltip from "@mui/material/Tooltip";
import {TypographyProps} from "@mui/material";

import { TaipyActiveProps, TaipyChangeProps, TaipyLabelProps } from "./utils";
import { getInitials } from "../../utils";
import { LovItem } from "../../utils/lov";
import { stringIcon, Icon } from "../../utils/icon";

export interface SelTreeProps extends LovProps, TaipyLabelProps {
    filter?: boolean;
    multiple?: boolean;
    width?: string | number;
    dropdown?: boolean;
}

export interface LovProps<T = string | string[], U = string> extends TaipyActiveProps, TaipyChangeProps {
    defaultLov?: string;
    lov?: LoV;
    value?: T;
    defaultValue?: U;
    height?: string | number;
    valueById?: boolean;
}

type LoVElt = [string, stringIcon, LoVElt[]?];

export type LoV = LoVElt[];

const getLovItem = (elt: LoVElt | string, tree = false): LovItem => {
    const it: LovItem = Array.isArray(elt)
        ? {
              id: elt[0],
              item: elt[1] || elt[0],
          }
        : { id: "" + elt, item: "" + elt };
    if (tree) {
        it.children = Array.isArray(elt) && elt.length > 2 ? elt[2]?.map((e) => getLovItem(e, true)) : [];
    }
    return it;
};

export const boxSx = { width: "100%" } as CSSProperties;
export const paperBaseSx = { width: "100%", mb: 2, display: "grid", gridTemplateRows: "auto 1fr" } as CSSProperties;
export const treeSelBaseSx = { width: "100%", bgcolor: "background.paper", overflowY: "auto" } as CSSProperties;

export const useLovListMemo = (lov: LoV | undefined, defaultLov: string, tree = false): LovItem[] =>
    useMemo(() => {
        if (lov) {
            if (!Array.isArray(lov)) {
                console.debug("lov wrong format ", lov);
                return [];
            }
            return lov.map((elt) => getLovItem(elt, tree));
        } else if (defaultLov) {
            let parsedLov;
            try {
                parsedLov = JSON.parse(defaultLov);
            } catch (e) {
                parsedLov = [];
            }
            return parsedLov.map((elt: LoVElt) => getLovItem(elt, tree));
        }
        return [];
    }, [lov, defaultLov, tree]);


const cardSx = { padding: 0 } as CSSProperties;
export const LovImage = ({ item, disableTypo, height, titleTypographyProps }: { item: Icon, disableTypo?: boolean, height?: string, titleTypographyProps?: TypographyProps }) => {
    const sx = useMemo(() => height ? {height: height, "& .MuiAvatar-img": { objectFit: "contain" }} : undefined, [height]);
    return (
    <CardHeader sx={cardSx} avatar={<Tooltip title={item.text}><Avatar alt={item.text} src={item.path} sx={sx} /></Tooltip>} title={item.text} disableTypography={disableTypo} titleTypographyProps={titleTypographyProps} />
)};

export const showItem = (elt: LovItem, searchValue: string) => {
    return (
        !searchValue ||
        ((typeof elt.item === "string" ? (elt.item as string) : (elt.item as Icon).text) || elt.id)
            .toLowerCase()
            .indexOf(searchValue.toLowerCase()) > -1
    );
};

export interface ItemProps {
    value: string;
    clickHandler: (evt: MouseEvent<HTMLElement>) => void;
    selectedValue: string[] | string;
    item: stringIcon;
    disabled: boolean;
    withAvatar?: boolean;
    titleTypographyProps?: TypographyProps;
}

export const SingleItem = ({ value, clickHandler, selectedValue, item, disabled, withAvatar = false, titleTypographyProps }: ItemProps) => (
    <ListItemButton
        onClick={clickHandler}
        data-id={value}
        selected={Array.isArray(selectedValue) ? selectedValue.indexOf(value) !== -1 : selectedValue === value}
        disabled={disabled}
    >
        {typeof item === "string" ? (
            withAvatar ? (
                <ListItemAvatar>
                    <CardHeader sx={cardSx} avatar={<Tooltip title={item}><Avatar>{getInitials(item)}</Avatar></Tooltip>} title={item} titleTypographyProps={titleTypographyProps} />
                </ListItemAvatar>
            ) : (
                <ListItemText primary={item} />
            )
        ) : (
            <ListItemAvatar>
                <LovImage item={item} titleTypographyProps={titleTypographyProps} />
            </ListItemAvatar>
        )}
    </ListItemButton>
);

export const isLovParent = (lov: LovItem[] | undefined, id: string, childId: string, path:string[] = []): boolean => {
    if (!lov) {
        return false;
    }
    for(let i = 0; i < lov.length; i++) {
        if (lov[i].id === id && !(lov[i].children || []).length) {
            return false;
        } else if (lov[i].id === childId) {
            return path.includes(id);
        } else if (isLovParent(lov[i].children, id, childId, [...path, lov[i].id])) {
             return true;
        }
    }
    return false;
}