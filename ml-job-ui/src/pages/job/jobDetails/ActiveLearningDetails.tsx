import {useParams} from 'react-router-dom';

import JobData from "./components/JobData.tsx";
import {useState} from "react";
import useJobExtended from "./hooks/useJobExtended.ts";
import SpectraSelector from "./components/activeLearning/spectraSelector/SpectraSelector.tsx";
import JobFiles from "./components/JobFiles.tsx";
import JobPhase from "../types/enums/jobPhase.ts";
import PreprocessedPlot from "./components/activeLearning/PreprocessedPlot.tsx";
import FitsDataAndPlot from "./components/activeLearning/fitsDataAndPlot/FitsDataAndPlot.tsx";
import useIteration from "./hooks/activeLearning/useIteration.ts";
import TrainingDataPlot from "./components/activeLearning/trainingDataPlot/TrainingDataPlot.tsx";
import PerfEstPlot from "./components/activeLearning/PerfEstPlot/PerfEstPlot.tsx";
import useJobFiles from "./hooks/useJobFiles.ts";

const ActiveLearningDetails = () => {
    const { jobId } = useParams();
    const {job, setJob, loading: jobLoading, error: jobError} = useJobExtended(jobId)
    const [currentSpectrum, setCurrentSpectrum] = useState("");
    const {iteration, error: iterError} = useIteration(job)
    const { files, loading: filesLoading, error: filesError, fetchData } = useJobFiles(job);
    if(jobLoading) return <p>Loading job...</p>;
    if(jobError) return <p>Error in job fetching: {jobError}</p>;
    return (
        <div>
            <JobData job={job} setJob={setJob}/>
            <div className="mt-5">
                <JobFiles job={job} files={files} loading={filesLoading} error={filesError}
                />
            </div>
            <div className="mt-3">
                {
                    iterError && <p className="text-red-800">{iterError}</p>
                }
                {
                    !iterError && iteration !== null &&
                    <div className="space-y-2">
                        <p className="font-bold">Iteration number: {iteration} </p>
                        {iteration !== 0 &&
                            <div className="space-y-2">
                                <TrainingDataPlot job={job}/>
                                <PerfEstPlot job={job}/>
                            </div>
                        }
                    </div>
                }
            </div>
            {
                job && job.phase === JobPhase.COMPLETED &&
                <div className="mt-5">
                    <div>
                        <SpectraSelector job={job} setCurrentSpectrum={setCurrentSpectrum}
                                         updateFiles={fetchData}
                                         iteration={iteration}/>
                        <PreprocessedPlot job={job} currentSpectrum={currentSpectrum}/>
                    </div>
                    <div className="mt-5">
                        <FitsDataAndPlot filename={currentSpectrum} />
                    </div>
                </div>
            }
            {/*                 currentInd={currentInd} setCurrentInd={setCurrentInd} />*/}
            {/*<AlPlot title={"Preprocessed spectra"} waves={data.waves} fluxes={currentSpectra.fluxes}/>*/}
            {/*<AlPlot title={"Raw spectra"} waves={currentSpectra.raw_waves}*/}
            {/*        fluxes={currentSpectra.raw_fluxes}/>*/}


        </div>

    );
};

export default ActiveLearningDetails;