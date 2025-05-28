import JobExtended from "../types/jobExtended.ts";
import {useCallback, useEffect, useState} from "react";
import FileEntry from "../../types/fileEntry.ts";
import config from "../../../../config.ts";

const useJobFiles = (job: JobExtended | null) => {
    const [files, setFiles] = useState<FileEntry[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const fetchData = useCallback(async () => {
        if (!job) return;

        setLoading(true);
        try {
            const dirPathQuery = encodeURIComponent(job.dir_path);
            const resp = await fetch(
                `${config.baseFileApi}/?parent_dir_path=${dirPathQuery}`
            );

            if (!resp.ok) {
                throw new Error("Error in job spectrum fetching: " + resp.statusText);
            }

            const data = await resp.json();
            setFiles(data.files);
            setError("");
        } catch (err) {
            setError(err instanceof Error ? err.message : "Unknown error in job fetching");
        } finally {
            setLoading(false);
        }
    }, [job]);
    
    useEffect(() => {
        fetchData()
    }, [fetchData]);


    return {files, loading, error, fetchData};
}


export default useJobFiles;