import {useCallback, useEffect, useState} from 'react';
import JobExtended from "../types/jobExtended.ts";
import config from "../../../../config.ts"
import JobPhase from "../../types/enums/jobPhase.ts";

const useJobExtended = (jobId: string | undefined) => {
    const [job, setJob] = useState<JobExtended | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string>("");

    const loadJob = useCallback(async () => {
        setLoading(true);
        setError("");
        try {
            setLoading(true);
            setError("");
            const response = await fetch(`${config.baseJobApi}/${jobId}`);
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            setJob(data);
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Unknown error in job fetching");
        } finally {
            setLoading(false);
        }
    }, [jobId]);
    
    useEffect(() => {
        loadJob();
    }, [jobId, loadJob]);

    useEffect(() => {
        if (job?.phase === JobPhase.PROCESSING) {
            const timer = setTimeout(() => {
                loadJob();
            }, 10000);

            return () => clearTimeout(timer);
        }
    }, [job, loadJob]);

    return { job, setJob, loading, error };
};

export default useJobExtended;
