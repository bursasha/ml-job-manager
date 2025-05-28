import React from 'react';
import Plot from "react-plotly.js";

interface Props {
    perfEst: number[]
    loading: boolean,
    error: string
}

const PerfLinearPlot: React.FC<Props> = ( {perfEst, loading, error} ) => {

    if(loading) return <p>Loading performance estimation plot</p>
    if(error) return <p className="text-red-800">{error}</p>
    if(!perfEst.length) return <p>Performance estimation list is empty.</p>

    return (
        <div>
            <Plot
                data={[
                    {
                        x: Array.from({length: perfEst.length}, (_, i) => i + 1),
                        y: perfEst,
                    }
                ]}
                layout={{
                    title: {text: "Performance estimation"},
                    xaxis: {
                        title: {text: "Iterations"},
                        zeroline: false,
                    },
                    yaxis: {
                        title: {text: "Performances"},
                        zeroline: false,
                    },
                    autosize: true
                }}
                style={{width: '100%', height: '100%'}}
            />
        </div>
    );
};

export default PerfLinearPlot;