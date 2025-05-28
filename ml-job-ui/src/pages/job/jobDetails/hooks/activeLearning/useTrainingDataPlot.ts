import {useEffect, useState} from "react";
import JobPhase from "../../../types/enums/jobPhase.ts";
import config from "../../../../../config.ts";
import TrainingDataTsne from "../../types/trainingDataTsne.ts";
import JobExtended from "../../types/jobExtended.ts";

const useTrainingDataPlot = (job: JobExtended| null) => {
    const [tsneData, setTsneData] = useState<TrainingDataTsne|null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const fetchData = async () => {
        if(!job || job.phase !== JobPhase.COMPLETED || tsneData)
            return

        setLoading(true)
        setError("")
        try {
            const dirPathQuery = encodeURIComponent(job.dir_path)
            const response = await fetch(`
                ${config.baseFileApi}/dim_reduc.json/download/?parent_dir_path=${dirPathQuery}`,
                {method: "GET",}
            );

            if(!response.ok)
                throw new Error("Error in fetching iteration: " + response.statusText);

            const data = await response.json();
            setTsneData(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Unknown error in fetch prep spectra");
        }
        finally {
            setLoading(false);
        }
    }

    return {fetchData, tsneData, loading, error};
}

export default useTrainingDataPlot;