import React from 'react';
import Plot from "react-plotly.js";

interface PlotProps {
    title: string;
    waves: number[];
    fluxes: number[];
}

const SpectrumPlot: React.FC<PlotProps> = ({title, waves, fluxes}) => {
    return (
        <div>
            <Plot
                data={[
                    {
                        x: waves,
                        y: fluxes,
                    }
                ]}
                layout={{
                    title: {text: title},
                    xaxis: {
                        title: {text: 'Wavelengths'},
                        zeroline: false
                    },
                    yaxis: {
                        title: {text: 'Fluxes'},
                        zeroline: false
                    },
                    autosize: true
                }}
                style={{width: '100%', height: '100%'}}
            />
        </div>
    );
};

export default SpectrumPlot;