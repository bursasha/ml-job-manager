import React, {useEffect, useState} from 'react';
import TrainingDataTsne from "../../../types/trainingDataTsne.ts";
import Plot from "react-plotly.js";
import { Data } from "plotly.js";
interface Props {
    dataTsne: TrainingDataTsne
}

const ScatterPlotTsne: React.FC<Props> = ({dataTsne}) => {
    const [plotData, setPlotData] = useState<Data[]>([]);
    useEffect(() => {
        if(!dataTsne)
            return;

        setPlotData(dataTsne.classes.map((c, i) => {
            return {
                x: dataTsne.x.filter((_, j) => dataTsne.labels[j] === i),
                y: dataTsne.y.filter((_, j) => dataTsne.labels[j] === i),
                name: c,
                type: "scatter" as const,
                mode: "markers" as const ,
            };
        }));
    }, [dataTsne]);

    return (
        <Plot
            data={plotData}
            layout={{
                title: "Training data scatter plot",
                legend: { orientation: 'h', xanchor: "center", x: 0.5},
                xaxis: { zeroline: false },
                yaxis: { zeroline: false },
            }}
            style={{ width: '70%'}}
            useResizeHandler
        />
    );
};

export default ScatterPlotTsne;