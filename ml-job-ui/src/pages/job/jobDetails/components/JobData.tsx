import React, {useState} from 'react';
import JobExtended from "../types/jobExtended.ts";
import JobPhase from "../../types/enums/jobPhase.ts";
import config from "../../../../config.ts";
import {useNavigate} from "react-router-dom";
import {formatDateTime} from "../../../../utils/dateTimeUtils.ts";

interface JobDataProps {
    job: JobExtended | null;
    setJob: (job: JobExtended) => void;
}

const JobData: React.FC<JobDataProps> = ({ job, setJob }) => {
    const navigate = useNavigate();
    const [error, setError] = useState("");

    const handleUserAction = async (action: string) => {
        try {
            setError("");
            const response = await fetch(`${config.baseJobApi}/${job?.job_id}/process/${action}`, {
                method: "POST",
            })
            if (!response.ok) {
                throw new Error("User action error: " + response.statusText);
            }
            const data = await response.json();
            setJob(data);
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Unknown error in user action");
        }
    }

    const handleJobDeletion = async () => {
        setError("");
        if(window.confirm("Are you sure you want to delete this job?")) {
            try {
                const response = await fetch(`${config.baseJobApi}/${job?.job_id}`, {
                    method: "DELETE",
                })
                if (!response.ok) {
                    throw new Error("User action error: " + response.statusText);
                }
                navigate("/jobs")
            } catch (err: unknown) {
                setError(err instanceof Error ? err.message : "Unknown error in job deletion");
            }
        }
    }

    return (
        <div>
            {error && <p className="text-red-800 mx-2">{error}</p>}
            <h1 className="text-3xl font-bold mb-4">{job?.label}</h1>
            <table className="table-auto min-w-full">
                <thead>
                <tr>
                    <th className="py-2 border bg-gray-300">Job id</th>
                    <th className="py-2 border bg-gray-300">Type</th>
                    <th className="py-2 border bg-gray-300">Phase</th>
                    <th className="py-2 border bg-gray-300">Created at</th>
                    <th className="py-2 border bg-gray-300">Started at</th>
                    <th className="py-2 border bg-gray-300">Ended at</th>
                    <th className="py-2 border bg-gray-300">Execution duration</th>
                </tr>
                </thead>
                <tbody>
                <tr key={job?.job_id}>
                    <td className="p-2 border text-center w-[25%]">{job?.job_id}</td>
                    <td className="p-2 border text-center">{job?.type}</td>
                    <td className="p-2 border text-center">{job?.phase}</td>
                    <td className="p-2 border text-center w-[15%]">
                        {job?.created_at ? formatDateTime(job.created_at) : ""}
                    </td>
                    <td className="p-2 border text-center w-[15%]">
                        {job?.started_at ? formatDateTime(job.started_at) : ""}
                    </td>
                    <td className="p-2 border text-center w-[15%]">
                        {job?.ended_at ? formatDateTime(job.ended_at) : ""}
                    </td>
                    <td className="p-2 border text-center">
                        {job?.execution_duration ? `${Math.round(job.execution_duration * 100) / 100} sec` : ""}
                    </td>
                </tr>
                </tbody>
            </table>
            {
                job?.description &&
                <div className="mt-5">
                    <p className="font-bold">Description:</p>
                    <p>{job.description}</p>
                </div>
            }

            <div className="flex space-x-4 mt-4">
                <button
                    onClick={() => handleUserAction("RUN")} disabled={job?.phase !== JobPhase.PENDING}
                    className="p-2 rounded cursor-pointer bg-blue-600
                    text-white disabled:opacity-50 hover:bg-blue-800"
                >
                    RUN
                </button>
                <button
                    onClick={() => handleUserAction("ABORT")} disabled={job?.phase !== JobPhase.PROCESSING}
                    className="p-2 rounded cursor-pointer bg-purple-600
                    text-white disabled:opacity-50 hover:bg-purple-800"
                >
                    ABORT
                </button>
                <button
                    onClick={() => handleJobDeletion()} disabled={job?.phase === JobPhase.PROCESSING}
                    className="p-2 rounded cursor-pointer bg-red-600
                    text-white disabled:opacity-50 hover:bg-red-800"
                >
                    DELETE
                </button>
            </div>
        </div>
    );
};

export default JobData;
