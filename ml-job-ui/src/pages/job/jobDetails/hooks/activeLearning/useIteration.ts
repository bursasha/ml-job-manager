import JobExtended from "../../types/jobExtended.ts";
import {useEffect, useState} from "react";
import JobPhase from "../../../types/enums/jobPhase.ts";
import config from "../../../../../config.ts";

const useIteration = (job: JobExtended | null) => {
    const [iteration, setIteration] = useState<number|null>(null);
    const [error, setError] = useState("");
    useEffect(() => {
        const fetchIteration = async () => {
            if(!job || job.phase !== JobPhase.COMPLETED)
                return

            setError("")
            try {
                const dirPathQuery = encodeURIComponent(job.dir_path)
                const response = await fetch(`
                ${config.baseFileApi}/config.json/download/?parent_dir_path=${dirPathQuery}`,
                    {method: "GET",}
                );

                if(!response.ok)
                    throw new Error("Error in fetching iteration: " + response.statusText);

                const data = await response.json();
                setIteration(data.iteration);
            } catch (err) {
                setError(err instanceof Error ? err.message : "Unknown error in fetch prep spectra");
            }
        }

        fetchIteration()
    }, [job])

    return {iteration, error}
}


export default useIteration;