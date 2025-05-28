import {useEffect, useState} from "react";
import config from "../../../../../config.ts";

const useClasses = (dirPath: string) => {
    const [classes, setClasses] = useState<string[]>([]);
    const [error, setError] = useState("");
    useEffect(() => {
        const fetchClasses = async () => {
            setError("")
            try {
                const dirPathQuery = encodeURIComponent(dirPath)
                const response = await fetch(`
                ${config.baseFileApi}/config.json/download/?parent_dir_path=${dirPathQuery}`,
                    {method: "GET",}
                );

                if(!response.ok)
                    throw new Error("Error in fetching classes: " + response.statusText);

                const data = await response.json();
                setClasses(data.classes);
            } catch (err) {
                setError(err instanceof Error ? err.message : "Unknown error in fetch prep spectra");
            }
        }

        fetchClasses()
    }, [dirPath])

    return {classes, error}
}

export default useClasses;