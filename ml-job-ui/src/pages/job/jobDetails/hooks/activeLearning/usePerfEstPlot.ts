import {useState} from "react";
import JobPhase from "../../../types/enums/jobPhase.ts";
import config from "../../../../../config.ts";
import JobExtended from "../../types/jobExtended.ts";

const usePerfEstPlot = (job: JobExtended | null) => {
    const [perfEst, setPerfEst] = useState<number[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const fetchData = async () => {
        if(!job || job.phase !== JobPhase.COMPLETED)
            return

        setLoading(true)
        setError("")
        try {
            const dirPathQuery = encodeURIComponent(job.dir_path)
            const response = await fetch(`
                ${config.baseFileApi}/perf_est_list.json/download/?parent_dir_path=${dirPathQuery}`,
                {method: "GET",}
            );

            if(!response.ok)
                throw new Error("Error in performance estimation list: " + response.statusText);

            const data: number[] = await response.json();
            setPerfEst(data.map(p => p * 100));
        } catch (err) {
            setError(err instanceof Error ? err.message : "Unknown error in fetching performance estimation list");
        }
        finally {
            setLoading(false);
        }
    }


    return {fetchData, perfEst, loading, error};
}

export default usePerfEstPlot;