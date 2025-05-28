import {useEffect, useState} from "react";
import FileEntry from "../../job/types/fileEntry.ts";
import config from "../../../config.ts";

const useFileSystem = (path: string) => {
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState("");
    const [files, setFiles] = useState<FileEntry[]>([]);
    const [directories, setDirectories] = useState<string[]>([]);

    useEffect(() => {
        const fetchFiles = async () => {
            setLoading(true);
            setError("");
            try {
                const query = encodeURIComponent(path);
                const response = await fetch(`${config.baseFileApi}/?parent_dir_path=${query}`, {
                    method: "GET",
                });
                const data = await response.json();
                setFiles(data.files);
                setDirectories(data.directories.map((d: { dirname: string }) => d.dirname));
            }
            catch(err: unknown) {
                setError(err instanceof Error ? err.message : "Unknown error in filesystem");
            }
            finally {
                setLoading(false);
            }
        }

        fetchFiles()
    }, [path]);


    return {files, setFiles, directories, setDirectories, loading, error};
}

export default useFileSystem;