import JobExtended from "../../types/jobExtended.ts";
import {useEffect, useState} from "react";
import JobPhase from "../../../types/enums/jobPhase.ts";
import Labelling from "../../types/labelling.ts";
import config from "../../../../../config.ts";

const useLabelling = (job: JobExtended) => {
    const [labellings, setLabellings] = useState<Labelling[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        console.log(job);
        const fetchLabellings = async () => {
            if(job.phase !== JobPhase.COMPLETED)
                return;
            try {
                const response = await fetch(`${config.baseLabellingApi}/?job_id=${job.job_id}`,
                    { method:"GET" }
                );

                if(!response.ok) {
                    throw new Error("Error in labellings fetching: " + response.statusText);
                }
                const data = await response.json();
                setLabellings(data.labellings);
            }
            catch (err: unknown) {
                setError(err instanceof Error ? err.message : "Unknown error in labelling fetching");
            }
            finally {
                setLoading(false);
            }



        }

        fetchLabellings()
    }, [job]);

    return {labellings, setLabellings , loading, error}
}

export default useLabelling;