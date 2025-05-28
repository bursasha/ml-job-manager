import React, {useState} from 'react';
import usePerfEstPlot from "../../../hooks/activeLearning/usePerfEstPlot.ts";
import JobExtended from "../../../types/jobExtended.ts";
import BlueButton from "../../../../../../components/buttons/BlueButton.tsx";
import PerfLinearPlot from "./PerfLinearPlot.tsx";

interface Props {
    job: JobExtended | null
}

const PerfEstPlot: React.FC<Props> = ({job}) => {
    const  {fetchData, perfEst, loading, error} = usePerfEstPlot(job)
    const [show, setShow] = useState(false)
    const handleClick = async () => {
        if(!show) {
            await fetchData();
        }
        setShow(prev => !prev);
    }
    return (
        <div className="space-y-2">
            <BlueButton onClick={handleClick}>
                {show ? "Hide" : "Show"} performance estimation plot
            </BlueButton>
            {
                show && <PerfLinearPlot perfEst={perfEst} loading={loading} error={error} />
            }
        </div>
    );
};

export default PerfEstPlot;