import React, {useState} from 'react';
import useTrainingDataPlot from "../../../hooks/activeLearning/useTrainingDataPlot.ts";
import JobExtended from "../../../types/jobExtended.ts";
import BlueButton from "../../../../../../components/buttons/BlueButton.tsx";
import ScatterPlotTsne from "./ScatterPlotTsne.tsx";

interface Props {
    job: JobExtended | null
}

const TrainingDataPlot: React.FC<Props> = ({job}) => {
    const {fetchData, tsneData, loading, error} = useTrainingDataPlot(job)
    const [show, setShow] = useState(false)
    const handleClick = async () => {
        if(!tsneData) {
            await fetchData()
        }

        setShow(prev => !prev);
    }

    return (
        <div className="space-y-2">
            <BlueButton onClick={handleClick}>
                {show ? "Hide" : "Show"} t-SNE plot
            </BlueButton>
            {
                show && loading && <p>Loading data for t-SNE plot</p>
            }
            {
                show && error && <p className="text-red-800">{error}</p>
            }
            {
                show && tsneData && <ScatterPlotTsne dataTsne={tsneData}/>
            }
        </div>
    );
};

export default TrainingDataPlot;