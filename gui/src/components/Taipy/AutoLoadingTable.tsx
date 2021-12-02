import React, { useState, useEffect, useContext, useCallback, useRef, useMemo, CSSProperties } from "react";
import Box from "@mui/material/Box";
import MuiTable from "@mui/material/Table";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TableSortLabel from "@mui/material/TableSortLabel";
import Paper from "@mui/material/Paper";
import { visuallyHidden } from "@mui/utils";
import AutoSizer from "react-virtualized-auto-sizer";
import { FixedSizeList as List } from "react-window";
import InfiniteLoader from "react-window-infinite-loader";
import Skeleton from "@mui/material/Skeleton";
import IconButton from "@mui/material/IconButton";
import AddIcon from "@mui/icons-material/Add";

import { TaipyContext } from "../../context/taipyContext";
import {
    createRequestInfiniteTableUpdateAction,
    createSendActionNameAction,
    FormatConfig,
} from "../../context/taipyReducers";
import {
    ColumnDesc,
    alignCell,
    getsortByIndex,
    Order,
    TaipyTableProps,
    boxSx,
    paperSx,
    tableSx,
    RowType,
    EditableCell,
    OnCellValidation,
    RowValue,
    EDIT_COL,
    OnRowDeletion,
    iconInRowSx,
    addDeleteColumn,
} from "./tableUtils";
import { useDispatchRequestUpdateOnFirstRender, useDynamicProperty, useFormatConfig } from "../../utils/hooks";

interface RowData {
    colsOrder: string[];
    columns: Record<string, ColumnDesc>;
    rows: RowType[];
    classes: Record<string, string>;
    cellStyles: CSSProperties[];
    isItemLoaded: (index: number) => boolean;
    selection: number[];
    formatConfig: FormatConfig;
    onValidation?: OnCellValidation;
    onDeletion?: OnRowDeletion;
}

const Row = ({
    index,
    style,
    data: {
        colsOrder,
        columns,
        rows,
        classes,
        cellStyles,
        isItemLoaded,
        selection,
        formatConfig,
        onValidation,
        onDeletion,
    },
}: {
    index: number;
    style: CSSProperties;
    data: RowData;
}) =>
    isItemLoaded(index) ? (
        <TableRow
            hover
            tabIndex={-1}
            key={"row" + index}
            component="div"
            sx={style}
            className={classes && classes.row}
            data-index={index}
            selected={selection.indexOf(index) > -1}
        >
            {colsOrder.map((col, cidx) => (
                <TableCell
                    component="div"
                    variant="body"
                    key={"val" + index + "-" + cidx}
                    {...alignCell(columns[col])}
                    sx={cellStyles[cidx]}
                >
                    <EditableCell
                        colDesc={columns[col]}
                        value={rows[index][col]}
                        formatConfig={formatConfig}
                        rowIndex={index}
                        onValidation={onValidation}
                        onDeletion={onDeletion}
                    />
                </TableCell>
            ))}
        </TableRow>
    ) : (
        <Skeleton sx={style} key={"Skeleton" + index} />
    );

interface PromiseProps {
    resolve: () => void;
    reject: () => void;
}

interface key2Rows {
    key: string;
    promises: Record<number, PromiseProps>;
}

const ROW_HEIGHT = 54;

const AutoLoadingTable = (props: TaipyTableProps) => {
    const {
        className,
        id,
        tp_varname,
        refresh = false,
        height = "60vh",
        tp_updatevars,
        selected = [],
        pageSize = 100,
        defaultKey = "",
        editAction = "",
        deleteAction = "",
        addAction = "",
    } = props;
    const [rows, setRows] = useState<RowType[]>([]);
    const [rowCount, setRowCount] = useState(1000); // need someting > 0 to bootstrap the infinit loader
    const { dispatch } = useContext(TaipyContext);
    const page = useRef<key2Rows>({ key: defaultKey, promises: {} });
    const [orderBy, setOrderBy] = useState("");
    const [order, setOrder] = useState<Order>("asc");
    const infiniteLoaderRef = useRef<InfiniteLoader>(null);
    const headerRow = useRef<HTMLTableRowElement>(null);
    const formatConfig = useFormatConfig();
    const [visibleStartIndex, setVisibleStartIndex] = useState(0);

    const active = useDynamicProperty(props.active, props.defaultActive, true);
    const editable = useDynamicProperty(props.editable, props.defaultEditable, true);

    useEffect(() => {
        if (props.value && page.current.key && props.value[page.current.key] !== undefined) {
            const newValue = props.value[page.current.key];
            const promise = page.current.promises[newValue.start];
            setRowCount(newValue.rowcount);
            const nr = newValue.data as RowType[];
            if (Array.isArray(nr) && nr.length > newValue.start) {
                setRows(nr);
                promise && promise.resolve();
            } else {
                promise && promise.reject();
            }
            delete page.current.promises[newValue.start];
        }
    }, [props.value]);

    useDispatchRequestUpdateOnFirstRender(dispatch, id, tp_updatevars);

    const handleRequestSort = useCallback(
        (event: React.MouseEvent<unknown>, col: string) => {
            const isAsc = orderBy === col && order === "asc";
            setOrder(isAsc ? "desc" : "asc");
            setOrderBy(col);
            setRows([]);
            setTimeout(() => infiniteLoaderRef.current?.resetloadMoreItemsCache(true), 1); // So that the state can be changed
        },
        [orderBy, order]
    );

    useEffect(() => {
        setRows([]);
        setTimeout(() => infiniteLoaderRef.current?.resetloadMoreItemsCache(true), 1); // So that the state can be changed
    }, [refresh]);

    const createSortHandler = useCallback(
        (col: string) => (event: React.MouseEvent<unknown>) => {
            handleRequestSort(event, col);
        },
        [handleRequestSort]
    );

    const [colsOrder, columns] = useMemo(() => {
        if (props.columns) {
            const columns = typeof props.columns === "string" ? JSON.parse(props.columns) : props.columns;
            addDeleteColumn(!!(active && editable && deleteAction), columns);
            return [Object.keys(columns).sort(getsortByIndex(columns)), columns];
        }
        return [[], {}];
    }, [active, editable, deleteAction, props.columns]);

    const boxBodySx = useMemo(() => ({ height: height }), [height]);

    useEffect(() => {
        selected.length &&
            infiniteLoaderRef.current &&
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            (infiniteLoaderRef.current as any)._listRef.scrollToItem(selected[0]);
    }, [selected]);

    useEffect(() => {
        if (headerRow.current) {
            Array.from(headerRow.current.cells).forEach((cell, idx) => {
                columns[colsOrder[idx]].width = cell.offsetWidth;
            });
        }
    }, [columns, colsOrder]);

    const loadMoreItems = useCallback(
        (startIndex: number, stopIndex: number) => {
            if (page.current.promises[startIndex]) {
                page.current.promises[startIndex].reject();
            }
            return new Promise<void>((resolve, reject) => {
                const key = `Infinite-${orderBy}-${order}`;
                page.current = {
                    key: key,
                    promises: { ...page.current.promises, [startIndex]: { resolve: resolve, reject: reject } },
                };
                const cols = colsOrder.map((col) => columns[col].dfid);
                dispatch(
                    createRequestInfiniteTableUpdateAction(
                        tp_varname,
                        id,
                        cols,
                        key,
                        startIndex,
                        stopIndex,
                        orderBy,
                        order
                    )
                );
            });
        },
        [tp_varname, orderBy, order, id, colsOrder, columns, dispatch]
    );

    const onAddRowClick = useCallback(
        () =>
            dispatch(
                createSendActionNameAction(tp_varname, {
                    action: addAction,
                    index: visibleStartIndex,
                })
            ),
        [visibleStartIndex, dispatch, tp_varname, addAction]
    );

    const isItemLoaded = useCallback((index: number) => index < rows.length && !!rows[index], [rows]);

    const onCellValidation: OnCellValidation = useCallback(
        (value: RowValue, rowIndex: number, colName: string) =>
            dispatch(
                createSendActionNameAction(tp_varname, {
                    action: editAction,
                    value: value,
                    index: rowIndex,
                    col: colName,
                })
            ),
        [dispatch, tp_varname, editAction]
    );

    const onRowDeletion: OnRowDeletion = useCallback(
        (rowIndex: number) =>
            dispatch(
                createSendActionNameAction(tp_varname, {
                    action: deleteAction,
                    index: rowIndex,
                })
            ),
        [dispatch, tp_varname, deleteAction]
    );

    const onTaipyItemsRendered = useCallback((onItemsR) => ({visibleStartIndex, visibleStopIndex}: {visibleStartIndex: number, visibleStopIndex: number}) => {
        setVisibleStartIndex(visibleStartIndex);
        onItemsR({visibleStartIndex,visibleStopIndex});
    }, []);

    const rowData: RowData = useMemo(
        () => ({
            colsOrder: colsOrder,
            columns: columns,
            rows: rows,
            classes: {},
            cellStyles: colsOrder.map((col) => ({ width: columns[col].width, height: ROW_HEIGHT - 32 })),
            isItemLoaded: isItemLoaded,
            selection: selected,
            formatConfig: formatConfig,
            onValidation: active && editable && editAction ? onCellValidation : undefined,
            onDeletion: active && editable && deleteAction ? onRowDeletion : undefined,
        }),
        [
            rows,
            isItemLoaded,
            active,
            editable,
            colsOrder,
            columns,
            selected,
            formatConfig,
            editAction,
            onCellValidation,
            deleteAction,
            onRowDeletion,
        ]
    );

    return (
        <Box sx={boxSx} id={id}>
            <Paper sx={paperSx}>
                <TableContainer>
                    <MuiTable
                        sx={tableSx}
                        aria-labelledby="tableTitle"
                        size={"medium"}
                        className={className}
                        stickyHeader={true}
                    >
                        <TableHead>
                            <TableRow ref={headerRow}>
                                {colsOrder.map((col, idx) => (
                                    <TableCell key={col + idx} sortDirection={orderBy === columns[col].dfid && order}>
                                        {columns[col].dfid === EDIT_COL ? (
                                            active && editable && addAction ? (
                                                <IconButton onClick={onAddRowClick} size="small" sx={iconInRowSx}>
                                                    <AddIcon />
                                                </IconButton>
                                            ) : null
                                        ) : (
                                            <TableSortLabel
                                                active={orderBy === columns[col].dfid}
                                                direction={orderBy === columns[col].dfid ? order : "asc"}
                                                onClick={createSortHandler(columns[col].dfid)}
                                                disabled={!active}
                                            >
                                                {columns[col].title === undefined
                                                    ? columns[col].dfid
                                                    : columns[col].title}
                                                {orderBy === columns[col].dfid ? (
                                                    <Box component="span" sx={visuallyHidden}>
                                                        {order === "desc" ? "sorted descending" : "sorted ascending"}
                                                    </Box>
                                                ) : null}
                                            </TableSortLabel>
                                        )}
                                    </TableCell>
                                ))}
                            </TableRow>
                        </TableHead>
                    </MuiTable>
                    <Box sx={boxBodySx}>
                        <AutoSizer>
                            {({ height, width }) => (
                                <InfiniteLoader
                                    ref={infiniteLoaderRef}
                                    isItemLoaded={isItemLoaded}
                                    itemCount={rowCount}
                                    loadMoreItems={loadMoreItems}
                                    minimumBatchSize={pageSize}
                                >
                                    {({ onItemsRendered, ref }) => (
                                        <List
                                            height={height}
                                            width={width}
                                            itemCount={rowCount}
                                            itemSize={ROW_HEIGHT}
                                            onItemsRendered={onTaipyItemsRendered(onItemsRendered)}
                                            ref={ref}
                                            itemData={rowData}
                                        >
                                            {Row}
                                        </List>
                                    )}
                                </InfiniteLoader>
                            )}
                        </AutoSizer>
                    </Box>
                </TableContainer>
            </Paper>
        </Box>
    );
};

export default AutoLoadingTable;
