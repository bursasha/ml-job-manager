import React from 'react';
import usePrepSpectra from "../../hooks/activeLearning/usePrepSpectra.ts";
import JobExtended from "../../types/jobExtended.ts";
import SpectrumPlot from "./SpectrumPlot.tsx";

interface Props {
    job: JobExtended;
    currentSpectrum: string;
}

const PreprocessedPlot: React.FC<Props> = ({job, currentSpectrum}) => {
    const { waves, spectra, loading, error } = usePrepSpectra(job)

    if(loading) return <p>Loading</p>;
    if(error) return <p className="text-red-800 my-2">{error}</p>;
    if(!(currentSpectrum in spectra)) return <p>{currentSpectrum} Preprocessed plot can not be displayed</p>
    return (
        <div>
            <SpectrumPlot title="Preprocessed spectrum" waves={waves} fluxes={spectra[currentSpectrum]}/>
        </div>
    );
};

export default PreprocessedPlot;