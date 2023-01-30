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

import React, {
    CSSProperties,
    useCallback,
    useContext,
    useEffect,
    useMemo,
    useRef,
    useState,
    lazy,
    Suspense,
} from "react";
import {
    Data,
    Layout,
    PlotMarker,
    PlotRelayoutEvent,
    PlotSelectionEvent,
    ScatterLine,
} from "plotly.js";
import Skeleton from "@mui/material/Skeleton";
import Box from "@mui/material/Box";
import Tooltip from "@mui/material/Tooltip";
import { useTheme } from "@mui/system";

import { TaipyContext } from "../../context/taipyContext";
import { getArrayValue, getUpdateVar, TaipyActiveProps, TaipyChangeProps } from "./utils";
import {
    createRequestChartUpdateAction,
    createSendActionNameAction,
    createSendUpdateAction,
} from "../../context/taipyReducers";
import { ColumnDesc } from "./tableUtils";
import { useClassNames, useDispatchRequestUpdateOnFirstRender, useDynamicProperty } from "../../utils/hooks";

const Plot = lazy(() => import("react-plotly.js"));

interface ChartProp extends TaipyActiveProps, TaipyChangeProps {
    title?: string;
    width?: string | number;
    height?: string | number;
    config: string;
    data?: Record<string, TraceValueType>;
    layout?: string;
    plotConfig?: string;
    onRangeChange?: string;
    testId?: string;
    render?: boolean;
    defaultRender?: boolean;
    template?: string;
    template_Dark_?: string;
    template_Light_?: string;
    //[key: `selected_${number}`]: number[];
}

interface ChartConfig {
    columns: Record<string, ColumnDesc>;
    labels: string[];
    modes: string[];
    types: string[];
    traces: string[][];
    xaxis: string[];
    yaxis: string[];
    markers: Partial<PlotMarker>[];
    selectedMarkers: Partial<PlotMarker>[];
    orientations: string[];
    names: string[];
    lines: Partial<ScatterLine>[];
    texts: string[];
    textAnchors: string[];
    options: Record<string, unknown>[];
    axisNames: Array<string[]>;
    addIndex: Array<boolean>;
    decimators?: string[];
}

export type TraceValueType = Record<string, (string | number)[]>;

const defaultStyle = { position: "relative", display: "inline-block" };

const indexedData = /^(\d+)\/(.*)/;

const getColNameFromIndexed = (colName: string): string => {
    const reRes = indexedData.exec(colName);
    if (reRes && reRes.length > 2) {
        return reRes[2] || colName;
    }
    return colName;
};

const getValue = <T,>(
    values: TraceValueType | undefined,
    arr: T[],
    idx: number,
    returnUndefined = false
): (string | number)[] | undefined => {
    const value = getValueFromCol(values, getArrayValue(arr, idx) as unknown as string);
    if (!returnUndefined || value.length) {
        return value;
    }
    return undefined;
};

const getValueFromCol = (values: TraceValueType | undefined, col: string): (string | number)[] => {
    if (values) {
        if (col) {
            if (Array.isArray(values)) {
                const reRes = indexedData.exec(col);
                if (reRes && reRes.length > 2) {
                    return values[parseInt(reRes[1], 10) || 0][reRes[2] || col] || [];
                }
            } else {
                return values[col] || [];
            }
        }
    }
    return [];
};

const getAxis = (traces: string[][], idx: number, columns: Record<string, ColumnDesc>, axis: number) => {
    if (traces.length > idx && traces[idx].length > axis && traces[idx][axis] && columns[traces[idx][axis]])
        return columns[traces[idx][axis]].dfid;
    return undefined;
};

const getDecimatorsPayload = (
    decimators: string[] | undefined,
    plotDiv: HTMLDivElement | null,
    modes: string[],
    columns: Record<string, ColumnDesc>,
    traces: string[][],
    relayoutData?: PlotRelayoutEvent
) => {
    return decimators
        ? {
              width: plotDiv?.clientWidth,
              height: plotDiv?.clientHeight,
              decimators: decimators.map((d, i) => d ? {
                decimator: d,
                xAxis: getAxis(traces, i, columns, 0),
                yAxis: getAxis(traces, i, columns, 1),
                zAxis: getAxis(traces, i, columns, 2),
                chartMode: modes[i]
              } : undefined),
              relayoutData: relayoutData,
          }
        : undefined;
};

const selectedPropRe = /selected(\d+)/;

const MARKER_TO_COL = ["color", "size", "symbol", "opacity"];

const Chart = (props: ChartProp) => {
    const {
        title = "",
        width = "100%",
        height,
        updateVarName,
        updateVars,
        id,
        data = {},
        onRangeChange,
        propagate = true,
    } = props;
    const { dispatch } = useContext(TaipyContext);
    const [selected, setSelected] = useState<number[][]>([]);
    const plotRef = useRef<HTMLDivElement>(null);
    const dataKey = useRef("default");
    const theme = useTheme();

    const refresh = data === null;
    const className = useClassNames(props.libClassName, props.dynamicClassName, props.className);
    const active = useDynamicProperty(props.active, props.defaultActive, true);
    const render = useDynamicProperty(props.render, props.defaultRender, true);
    const hover = useDynamicProperty(props.hoverText, props.defaultHoverText, undefined);

    // get props.selected[i] values
    useEffect(() => {
        setSelected((sel) => {
            Object.keys(props).forEach((key) => {
                const res = selectedPropRe.exec(key);
                if (res && res.length == 2) {
                    const idx = parseInt(res[1], 10);
                    let val = (props as unknown as Record<string, number[]>)[key];
                    if (val !== undefined) {
                        if (typeof val === "string") {
                            try {
                                val = JSON.parse(val) as number[];
                            } catch (e) {
                                // too bad
                                val = [];
                            }
                        }
                        if (!Array.isArray(val)) {
                            val = [];
                        }
                        if (
                            idx >= sel.length ||
                            val.length !== sel[idx].length ||
                            val.some((v, i) => sel[idx][i] != v)
                        ) {
                            sel = sel.concat();
                            sel[idx] = val;
                        }
                    }
                }
            });
            return sel;
        });
    }, [props]);

    const config = useMemo(() => {
        if (props.config) {
            try {
                return JSON.parse(props.config) as ChartConfig;
            } catch (e) {
                console.info(`Error while parsing Chart.config\n${(e as Error).message || e}`);
            }
        }
        return {
            columns: {} as Record<string, ColumnDesc>,
            labels: [],
            modes: [],
            types: [],
            traces: [],
            xaxis: [],
            yaxis: [],
            markers: [],
            selectedMarkers: [],
            orientations: [],
            names: [],
            lines: [],
            texts: [],
            textAnchors: [],
            options: [],
            axisNames: [],
            addIndex: [],
        } as ChartConfig;
    }, [props.config]);

    useEffect(() => {
        if (refresh || !data[dataKey.current]) {
            const backCols = Object.values(config.columns).map((col) => col.dfid);
            dataKey.current = backCols.join("-") + (config.decimators ? `--${config.decimators.join("")}` : "");
            dispatch(
                createRequestChartUpdateAction(
                    updateVarName,
                    id,
                    backCols,
                    dataKey.current,
                    getDecimatorsPayload(config.decimators, plotRef.current, config.modes, config.columns, config.traces)
                )
            );
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [refresh, dispatch, config.columns, config.traces, config.modes, config.decimators, updateVarName, id]);

    useDispatchRequestUpdateOnFirstRender(dispatch, id, updateVars);

    const layout = useMemo(() => {
        let playout = {} as Layout;
        if (props.layout) {
            try {
                playout = JSON.parse(props.layout);
            } catch (e) {
                console.info(`Error while parsing Chart.layout\n${(e as Error).message || e}`);
            }
        }
        let template = undefined;
        try {
            const tpl = props.template && JSON.parse(props.template);
            const tplTheme = theme.palette.mode === "dark" ? (props.template_Dark_ ? JSON.parse(props.template_Dark_) : darkTemplate) : props.template_Light_ && JSON.parse(props.template_Light_);
            template = tpl ? tplTheme ? {...tpl, ...tplTheme} : tpl : tplTheme ? tplTheme : undefined;
        } catch (e) {
            console.info(`Error while parsing Chart.template\n${(e as Error).message || e}`);
        }
        if (template) {
            playout.template = template;
        }
        return {
            ...playout,
            title: title || playout.title,
            xaxis: {
                title:
                    config.traces.length && config.traces[0].length && config.traces[0][0]
                        ? getColNameFromIndexed(config.columns[config.traces[0][0]].dfid)
                        : undefined,
                ...playout.xaxis,
            },
            yaxis: {
                title:
                    config.traces.length == 1 && config.traces[0].length > 1 && config.columns[config.traces[0][1]]
                        ? getColNameFromIndexed(config.columns[config.traces[0][1]].dfid)
                        : undefined,
                ...playout.yaxis,
            },
            clickmode: "event+select",
        } as Layout;
    }, [theme.palette.mode, title, config.columns, config.traces, props.layout, props.template, props.template_Dark_, props.template_Light_]);

    const style = useMemo(
        () =>
            height === undefined
                ? ({ ...defaultStyle, width: width } as CSSProperties)
                : ({ ...defaultStyle, width: width, height: height } as CSSProperties),
        [width, height]
    );
    const skelStyle = useMemo(() => ({ ...style, minHeight: "7em" }), [style]);

    const dataPl = useMemo(() => {
        const datum = data && data[dataKey.current];
        return config.traces.map((trace, idx) => {
            const ret = {
                ...getArrayValue(config.options, idx, {}),
                type: config.types[idx],
                mode: config.modes[idx],
                name:
                    getArrayValue(config.names, idx) ||
                    (config.columns[trace[1]] ? getColNameFromIndexed(config.columns[trace[1]].dfid) : undefined),
            } as Record<string, unknown>;
                ret.marker = getArrayValue(config.markers, idx, ret.marker || {});
                MARKER_TO_COL.forEach(prop => {
                    const val = (ret.marker as Record<string, unknown>)[prop];
                    if (val !== undefined && typeof val === "string") {
                        const arr = getValueFromCol(datum, val as string);
                        if (arr.length) {
                            (ret.marker as Record<string, unknown>)[prop] = arr;
                        }
                    }
                });
                const xs = getValue(datum, trace, 0) || [];
                const ys = getValue(datum, trace, 1) || [];
                const addIndex = getArrayValue(config.addIndex, idx, true) && !ys.length;
                const baseX = addIndex ? Array.from(Array(xs.length).keys()) : xs;
                const baseY = addIndex ? xs : ys;
                const axisNames = config.axisNames.length > idx ? config.axisNames[idx] : [] as string[];
                if (baseX.length) {
                    if (axisNames.length > 0 ) {
                        ret[axisNames[0]] = baseX;
                    } else {
                        ret.x = baseX;
                    }
                }
                if (baseY.length) {
                    if (axisNames.length > 1) {
                        ret[axisNames[1]] = baseY;
                    } else {
                        ret.y = baseY;
                    }
                }
                const baseZ = getValue(datum, trace, 2, true);
                if (baseZ) {
                    if (axisNames.length > 2) {
                        ret[axisNames[2]] = baseZ;
                    } else {
                        ret.z = baseZ;
                    }
                }
                for (let i = 3; i < axisNames.length; i++) {
                    ret[axisNames[i]] = getValue(datum, trace, i, true);
                }
                ret.text = getValue(datum, config.texts, idx, true);
                ret.xaxis = config.xaxis[idx];
                ret.yaxis = config.yaxis[idx];
                ret.hovertext = getValue(datum, config.labels, idx, true);
                const selPoints = getArrayValue(selected, idx, []);
                if (selPoints?.length) {
                    ret.selectedpoints = selPoints;
                }
                ret.orientation = getArrayValue(config.orientations, idx);
                ret.line = getArrayValue(config.lines, idx);
                ret.textposition = getArrayValue(config.textAnchors, idx);
            const selectedMarker = getArrayValue(config.selectedMarkers, idx);
            if (selectedMarker) {
                ret.selected = { marker: selectedMarker };
            }
            return ret as Data;
        });
    }, [data, config, selected]);

    const plotConfig = useMemo(() => {
        let plconf = {};
        if (props.plotConfig) {
            try {
                plconf = JSON.parse(props.plotConfig);
            } catch (e) {
                console.info(`Error while parsing Chart.plot_config\n${(e as Error).message || e}`);
            }
            if (typeof plconf !== "object" || plconf === null || Array.isArray(plconf)) {
                console.info("Error Chart.plot_config is not a dictionnary");
                plconf = {};
            }
        }
        if (active) {
            return plconf;
        } else {
            return { ...plconf, staticPlot: true };
        }
    }, [active, props.plotConfig]);

    const onRelayout = useCallback(
        (eventData: PlotRelayoutEvent) => {
            if (Object.keys(eventData).some(k => k.startsWith("xaxis."))) {
                onRangeChange && dispatch(createSendActionNameAction(id, { action: onRangeChange, ...eventData }));
                if (config.decimators && !config.types.includes("scatter3d")) {
                    const backCols = Object.values(config.columns).map((col) => col.dfid);
                    const eventDataKey = Object.entries(eventData)
                        .map(([k, v]) => `${k}=${v}`)
                        .join("-");
                    dataKey.current = backCols.join("-") + (config.decimators ? `--${config.decimators.join("")}` : "") + "--" + eventDataKey;
                    dispatch(
                        createRequestChartUpdateAction(
                            updateVarName,
                            id,
                            backCols,
                            dataKey.current,
                            getDecimatorsPayload(
                                config.decimators,
                                plotRef.current,
                                config.modes,
                                config.columns,
                                config.traces,
                                eventData
                            )
                        )
                    );
                }
            }
        },
        [
            dispatch,
            onRangeChange,
            id,
            config.modes,
            config.columns,
            config.traces,
            config.types,
            config.decimators,
            updateVarName,
        ]
    );

    const onAfterPlot = useCallback(() => {
        // Manage loading Animation ... One day
    }, []);

    const getRealIndex = useCallback(
        (index: number) => (data[dataKey.current].tp_index ? (data[dataKey.current].tp_index[index] as number) : index),
        [data]
    );

    const onSelect = useCallback(
        (evt?: PlotSelectionEvent) => {
            if (updateVars) {
                const traces = (evt?.points || []).reduce((tr, pt) => {
                    tr[pt.curveNumber] = tr[pt.curveNumber] || [];
                    tr[pt.curveNumber].push(getRealIndex(pt.pointIndex));
                    return tr;
                }, [] as number[][]);
                if (traces.length) {
                    traces.forEach((tr, idx) => {
                        const upvar = getUpdateVar(updateVars, `selected${idx}`);
                        if (upvar && tr && tr.length) {
                            dispatch(createSendUpdateAction(upvar, tr, props.onChange, propagate));
                        }
                    });
                } else if (config.traces.length === 1) {
                    const upvar = getUpdateVar(updateVars, 'selected0');
                    if (upvar) {
                        dispatch(createSendUpdateAction(upvar, [], props.onChange, propagate));
                    }
                }
            }
        },
        [getRealIndex, dispatch, updateVars, propagate, props.onChange, config.traces.length]
    );

    return render ? (
        <Box id={id} key="div" data-testid={props.testId} className={className} ref={plotRef}>
            <Tooltip title={hover || ""}>
                <Suspense fallback={<Skeleton key="skeleton" sx={skelStyle} />}>
                    <Plot
                        data={dataPl}
                        layout={layout}
                        style={style}
                        onRelayout={onRelayout}
                        onAfterPlot={onAfterPlot}
                        onSelected={onSelect}
                        onDeselect={onSelect}
                        config={plotConfig}
                    />
                </Suspense>
            </Tooltip>
        </Box>
    ) : null;
};

export default Chart;


const darkTemplate = {
    "data": {
        "barpolar": [
            {
                "marker": {
                    "line": {
                        "color": "rgb(17,17,17)"
                    },
                    "pattern": {
                        "solidity": 0.2
                    }
                },
                "type": "barpolar"
            }
        ],
        "bar": [
            {
                "error_x": {
                    "color": "#f2f5fa"
                },
                "error_y": {
                    "color": "#f2f5fa"
                },
                "marker": {
                    "line": {
                        "color": "rgb(17,17,17)"
                    },
                    "pattern": {
                        "solidity": 0.2
                    }
                },
                "type": "bar"
            }
        ],
        "carpet": [
            {
                "aaxis": {
                    "endlinecolor": "#A2B1C6",
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "minorgridcolor": "#506784",
                    "startlinecolor": "#A2B1C6"
                },
                "baxis": {
                    "endlinecolor": "#A2B1C6",
                    "gridcolor": "#506784",
                    "linecolor": "#506784",
                    "minorgridcolor": "#506784",
                    "startlinecolor": "#A2B1C6"
                },
                "type": "carpet"
            }
        ],
        "contour": [
            {
                "colorscale": [
                    [
                        0.0,
                        "#0d0887"
                    ],
                    [
                        0.1111111111111111,
                        "#46039f"
                    ],
                    [
                        0.2222222222222222,
                        "#7201a8"
                    ],
                    [
                        0.3333333333333333,
                        "#9c179e"
                    ],
                    [
                        0.4444444444444444,
                        "#bd3786"
                    ],
                    [
                        0.5555555555555556,
                        "#d8576b"
                    ],
                    [
                        0.6666666666666666,
                        "#ed7953"
                    ],
                    [
                        0.7777777777777778,
                        "#fb9f3a"
                    ],
                    [
                        0.8888888888888888,
                        "#fdca26"
                    ],
                    [
                        1.0,
                        "#f0f921"
                    ]
                ],
                "type": "contour"
            }
        ],
        "heatmapgl": [
            {
                "colorscale": [
                    [
                        0.0,
                        "#0d0887"
                    ],
                    [
                        0.1111111111111111,
                        "#46039f"
                    ],
                    [
                        0.2222222222222222,
                        "#7201a8"
                    ],
                    [
                        0.3333333333333333,
                        "#9c179e"
                    ],
                    [
                        0.4444444444444444,
                        "#bd3786"
                    ],
                    [
                        0.5555555555555556,
                        "#d8576b"
                    ],
                    [
                        0.6666666666666666,
                        "#ed7953"
                    ],
                    [
                        0.7777777777777778,
                        "#fb9f3a"
                    ],
                    [
                        0.8888888888888888,
                        "#fdca26"
                    ],
                    [
                        1.0,
                        "#f0f921"
                    ]
                ],
                "type": "heatmapgl"
            }
        ],
        "heatmap": [
            {
                "colorscale": [
                    [
                        0.0,
                        "#0d0887"
                    ],
                    [
                        0.1111111111111111,
                        "#46039f"
                    ],
                    [
                        0.2222222222222222,
                        "#7201a8"
                    ],
                    [
                        0.3333333333333333,
                        "#9c179e"
                    ],
                    [
                        0.4444444444444444,
                        "#bd3786"
                    ],
                    [
                        0.5555555555555556,
                        "#d8576b"
                    ],
                    [
                        0.6666666666666666,
                        "#ed7953"
                    ],
                    [
                        0.7777777777777778,
                        "#fb9f3a"
                    ],
                    [
                        0.8888888888888888,
                        "#fdca26"
                    ],
                    [
                        1.0,
                        "#f0f921"
                    ]
                ],
                "type": "heatmap"
            }
        ],
        "histogram2dcontour": [
            {
                "colorscale": [
                    [
                        0.0,
                        "#0d0887"
                    ],
                    [
                        0.1111111111111111,
                        "#46039f"
                    ],
                    [
                        0.2222222222222222,
                        "#7201a8"
                    ],
                    [
                        0.3333333333333333,
                        "#9c179e"
                    ],
                    [
                        0.4444444444444444,
                        "#bd3786"
                    ],
                    [
                        0.5555555555555556,
                        "#d8576b"
                    ],
                    [
                        0.6666666666666666,
                        "#ed7953"
                    ],
                    [
                        0.7777777777777778,
                        "#fb9f3a"
                    ],
                    [
                        0.8888888888888888,
                        "#fdca26"
                    ],
                    [
                        1.0,
                        "#f0f921"
                    ]
                ],
                "type": "histogram2dcontour"
            }
        ],
        "histogram2d": [
            {
                "colorscale": [
                    [
                        0.0,
                        "#0d0887"
                    ],
                    [
                        0.1111111111111111,
                        "#46039f"
                    ],
                    [
                        0.2222222222222222,
                        "#7201a8"
                    ],
                    [
                        0.3333333333333333,
                        "#9c179e"
                    ],
                    [
                        0.4444444444444444,
                        "#bd3786"
                    ],
                    [
                        0.5555555555555556,
                        "#d8576b"
                    ],
                    [
                        0.6666666666666666,
                        "#ed7953"
                    ],
                    [
                        0.7777777777777778,
                        "#fb9f3a"
                    ],
                    [
                        0.8888888888888888,
                        "#fdca26"
                    ],
                    [
                        1.0,
                        "#f0f921"
                    ]
                ],
                "type": "histogram2d"
            }
        ],
        "histogram": [
            {
                "marker": {
                    "pattern": {
                        "solidity": 0.2
                    }
                },
                "type": "histogram"
            }
        ],
        "scatter": [
            {
                "marker": {
                    "line": {
                        "color": "#283442"
                    }
                },
                "type": "scatter"
            }
        ],
        "scattergl": [
            {
                "marker": {
                    "line": {
                        "color": "#283442"
                    }
                },
                "type": "scattergl"
            }
        ],
        "surface": [
            {
                "colorscale": [
                    [
                        0.0,
                        "#0d0887"
                    ],
                    [
                        0.1111111111111111,
                        "#46039f"
                    ],
                    [
                        0.2222222222222222,
                        "#7201a8"
                    ],
                    [
                        0.3333333333333333,
                        "#9c179e"
                    ],
                    [
                        0.4444444444444444,
                        "#bd3786"
                    ],
                    [
                        0.5555555555555556,
                        "#d8576b"
                    ],
                    [
                        0.6666666666666666,
                        "#ed7953"
                    ],
                    [
                        0.7777777777777778,
                        "#fb9f3a"
                    ],
                    [
                        0.8888888888888888,
                        "#fdca26"
                    ],
                    [
                        1.0,
                        "#f0f921"
                    ]
                ],
                "type": "surface"
            }
        ],
        "table": [
            {
                "cells": {
                    "fill": {
                        "color": "#506784"
                    },
                    "line": {
                        "color": "rgb(17,17,17)"
                    }
                },
                "header": {
                    "fill": {
                        "color": "#2a3f5f"
                    },
                    "line": {
                        "color": "rgb(17,17,17)"
                    }
                },
                "type": "table"
            }
        ]
    },
    "layout": {
        "annotationdefaults": {
            "arrowcolor": "#f2f5fa"
        },
        "colorscale": {
            "diverging": [
                [
                    0,
                    "#8e0152"
                ],
                [
                    0.1,
                    "#c51b7d"
                ],
                [
                    0.2,
                    "#de77ae"
                ],
                [
                    0.3,
                    "#f1b6da"
                ],
                [
                    0.4,
                    "#fde0ef"
                ],
                [
                    0.5,
                    "#f7f7f7"
                ],
                [
                    0.6,
                    "#e6f5d0"
                ],
                [
                    0.7,
                    "#b8e186"
                ],
                [
                    0.8,
                    "#7fbc41"
                ],
                [
                    0.9,
                    "#4d9221"
                ],
                [
                    1,
                    "#276419"
                ]
            ],
            "sequential": [
                [
                    0.0,
                    "#0d0887"
                ],
                [
                    0.1111111111111111,
                    "#46039f"
                ],
                [
                    0.2222222222222222,
                    "#7201a8"
                ],
                [
                    0.3333333333333333,
                    "#9c179e"
                ],
                [
                    0.4444444444444444,
                    "#bd3786"
                ],
                [
                    0.5555555555555556,
                    "#d8576b"
                ],
                [
                    0.6666666666666666,
                    "#ed7953"
                ],
                [
                    0.7777777777777778,
                    "#fb9f3a"
                ],
                [
                    0.8888888888888888,
                    "#fdca26"
                ],
                [
                    1.0,
                    "#f0f921"
                ]
            ],
            "sequentialminus": [
                [
                    0.0,
                    "#0d0887"
                ],
                [
                    0.1111111111111111,
                    "#46039f"
                ],
                [
                    0.2222222222222222,
                    "#7201a8"
                ],
                [
                    0.3333333333333333,
                    "#9c179e"
                ],
                [
                    0.4444444444444444,
                    "#bd3786"
                ],
                [
                    0.5555555555555556,
                    "#d8576b"
                ],
                [
                    0.6666666666666666,
                    "#ed7953"
                ],
                [
                    0.7777777777777778,
                    "#fb9f3a"
                ],
                [
                    0.8888888888888888,
                    "#fdca26"
                ],
                [
                    1.0,
                    "#f0f921"
                ]
            ]
        },
        "colorway": [
            "#636efa",
            "#EF553B",
            "#00cc96",
            "#ab63fa",
            "#FFA15A",
            "#19d3f3",
            "#FF6692",
            "#B6E880",
            "#FF97FF",
            "#FECB52"
        ],
        "font": {
            "color": "#f2f5fa"
        },
        "geo": {
            "bgcolor": "rgb(17,17,17)",
            "lakecolor": "rgb(17,17,17)",
            "landcolor": "rgb(17,17,17)",
            "subunitcolor": "#506784"
        },
        "mapbox": {
            "style": "dark"
        },
        "paper_bgcolor": "rgb(17,17,17)",
        "plot_bgcolor": "rgb(17,17,17)",
        "polar": {
            "angularaxis": {
                "gridcolor": "#506784",
                "linecolor": "#506784"
            },
            "bgcolor": "rgb(17,17,17)",
            "radialaxis": {
                "gridcolor": "#506784",
                "linecolor": "#506784"
            }
        },
        "scene": {
            "xaxis": {
                "backgroundcolor": "rgb(17,17,17)",
                "gridcolor": "#506784",
                "linecolor": "#506784",
                "zerolinecolor": "#C8D4E3"
            },
            "yaxis": {
                "backgroundcolor": "rgb(17,17,17)",
                "gridcolor": "#506784",
                "linecolor": "#506784",
                "zerolinecolor": "#C8D4E3"
            },
            "zaxis": {
                "backgroundcolor": "rgb(17,17,17)",
                "gridcolor": "#506784",
                "linecolor": "#506784",
                "showbackground": true,
                "zerolinecolor": "#C8D4E3"
            }
        },
        "shapedefaults": {
            "line": {
                "color": "#f2f5fa"
            }
        },
        "sliderdefaults": {
            "bgcolor": "#C8D4E3",
            "bordercolor": "rgb(17,17,17)"
        },
        "ternary": {
            "aaxis": {
                "gridcolor": "#506784",
                "linecolor": "#506784"
            },
            "baxis": {
                "gridcolor": "#506784",
                "linecolor": "#506784"
            },
            "bgcolor": "rgb(17,17,17)",
            "caxis": {
                "gridcolor": "#506784",
                "linecolor": "#506784"
            }
        },
        "updatemenudefaults": {
            "bgcolor": "#506784"
        },
        "xaxis": {
            "gridcolor": "#283442",
            "linecolor": "#506784",
            "tickcolor": "#506784",
            "zerolinecolor": "#283442"
        },
        "yaxis": {
            "gridcolor": "#283442",
            "linecolor": "#506784",
            "tickcolor": "#506784",
            "zerolinecolor": "#283442"
        }
    }
};
