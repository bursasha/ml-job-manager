import React, {useState} from 'react';
import {saveAs} from 'file-saver'

import JobExtended from "../types/jobExtended.ts";
import config from "../../../../config.ts";
import FileEntry from "../../types/fileEntry.ts";

interface Props {
    job: JobExtended | null,
    files: FileEntry[],
    loading: boolean,
    error: string
}

const JobFiles: React.FC<Props> = ({job, files, loading, error}) => {
    const [downloadError, setDownloadError] = useState("");

    const handleDownload = async (filename: string) => {
        try {
            if(!job)
                throw new Error("Job is null in file downloading")

            const dirPathQuery = encodeURIComponent(job.dir_path)
            const response = await fetch(`
                ${config.baseFileApi}/${filename}/download/?parent_dir_path=${dirPathQuery}`,
                {
                    method: "GET",
            });
            if(!response.ok) {
                throw new Error("Error in fetching files: " + response.statusText);
            }

            const blob = await response.blob();

            saveAs(blob, filename);
        }
        catch (err: unknown){
            setDownloadError(err instanceof Error ? err.message : `Unknown error downloading file: ${filename}`);
        }
    }

    if(loading) return <p>Loading files</p>
    if(error) return <p className="text-red-800">Error in fetching files: {error}</p>
    return (
        <div className="space-y-2">
            {downloadError && <p className="text-red-800">{downloadError}</p>}
            <div>
                <p className="font-bold mb-1">Job's directory:</p>
                {job?.dir_path}
            </div>
            <p className="font-bold">Job's files:</p>
            <table className="table-auto w-[50%] border-collapse">
                <thead>
                <tr>
                    <td className="p-2 bg-gray-300 text-center border w-[40%]">Filename</td>
                    <td className="p-2 bg-gray-300 text-center border w-[30%]">Size</td>
                    <td className="p-2 bg-gray-300 text-center border w-[30%]">Download</td>
                </tr>
                </thead>
                <tbody>
                {
                    files.map((f, i) => (
                        <tr key={i}>
                            <td className="p-2 text-center border">
                                {f.filename}
                            </td>
                            <td className="p-2 text-center border">
                                {f.size} B
                            </td>
                            <td className="p-2 text-center border">
                                <button className="px-4 bg-blue-600 text-white rounded
                                        cursor-pointer disabled:opacity-50 hover:bg-blue-800"
                                        onClick={() => handleDownload(f.filename)}
                                >
                                    Download
                                </button>
                            </td>
                        </tr>
                    ))
                }
                </tbody>
            </table>
        </div>
    )
        ;
};

export default JobFiles;