import React, {useEffect, useState} from 'react';
import Selector from "./Selector.tsx";
import FillingData from "./FillingData.tsx";
import useLabeling from "../../../hooks/activeLearning/useLabelling.ts";
import JobExtended from "../../../types/jobExtended.ts";
import LabellingData from "./LabellingData.tsx";

interface Props {
    job: JobExtended;
    setCurrentSpectrum: (currentInd: string) => void;
    updateFiles: () => void;
    iteration: number | null;
}

const SpectraSelector: React.FC<Props> = ({job, setCurrentSpectrum, updateFiles, iteration}) => {
    const {labellings, setLabellings, loading, error} = useLabeling(job)
    const [currentInd, setCurrentInd] = useState(0);
    useEffect(() => {
        // console.log(currentInd)
        // console.log(labellings)
        if(labellings.length <= 0)
            return
        setCurrentSpectrum(labellings[currentInd].spectrum_filename)
    }, [currentInd, labellings, setCurrentSpectrum]);

    if(loading) return <p>Loadings labellings</p>
    if(error) return <p>Error in labellings: {error}</p>;
    return (
        <div className="bg-gray-100 p-2">
            <div className="flex ">
                <div className="w-[30%]">
                    <Selector labellings={labellings}
                              currentInd={currentInd} setCurrentInd={setCurrentInd}/>
                </div>
                <div className="ml-15">
                    <FillingData labellings={labellings} setLabellings={setLabellings}
                                 currentInd={currentInd} setCurrentInd={setCurrentInd}
                                dirPath={job.dir_path} updateFiles={updateFiles}
                                iteration={iteration}/>
                </div>
            </div>
            <div className={"my-5"}>
                <LabellingData labelling={labellings[currentInd]}/>
            </div>
        </div>

    );
};

export default SpectraSelector;