import React from 'react';

import Job from "../../../types/job.ts";
import JobPhase from "../../../types/enums/jobPhase.ts";
import jobPhase from "../../../types/enums/jobPhase.ts";
import JobType from "../../../types/enums/jobType.ts";
import {useNavigate} from "react-router-dom";
import BlueButton from "../../../../../components/buttons/BlueButton.tsx";
import {formatDateTime} from "../../../../../utils/dateTimeUtils.ts";

interface JobsTableProps {
    jobs: Job[];
}

const JobsTable: React.FC<JobsTableProps> = ({ jobs }) => {
    const navigate = useNavigate();

    const handleView = (job: Job) => {
        console.log(job)
        if (job.type === JobType.ACTIVE_ML) {
            navigate(`/jobs/details/active_learning/${job.job_id}`);
        }
         else if (job.type === JobType.DATA_PREPROCESSING)
            navigate(`/jobs/details/preprocessing/${job.job_id}`);
    };

    const getBGForJob = (phase: JobPhase) => {
        if(phase === jobPhase.PENDING)
            return "bg-white";
        if(phase === jobPhase.PROCESSING)
            return "bg-yellow-500";
        if(phase === jobPhase.COMPLETED)
            return "bg-green-500";
        if(phase === jobPhase.ERROR)
            return "bg-red-500";

        return "bg-purple-500";
     }

     const getDateTime = (dateTime: string) => {
        return dateTime ? formatDateTime(dateTime) : "";
     }

    return (
        <div>
            <table className="table-auto min-w-full border-collapse">
                <thead>
                    <tr>
                        <th className="py-2 bg-gray-300 border">Phase</th>
                        <th className="py-2 bg-gray-300 border">Type</th>
                        <th className="py-2 bg-gray-300 border">Job id</th>
                        <th className="py-2 bg-gray-300 border">Label</th>
                        <th className="py-2 bg-gray-300 border">Created at</th>
                        <th className="py-2 bg-gray-300 border">Started at</th>
                        <th className="py-2 bg-gray-300 border">Ended at</th>
                        <th className="py-2 bg-gray-300 border">Execution duration</th>
                        <th className="py-2 bg-gray-300 border">View</th>
                    </tr>
                </thead>
                <tbody>
                {
                    jobs.map(job => (
                        <tr key={job.job_id} className={`${getBGForJob(job.phase)}`}>
                            <td className="p-2 text-center border">{job.phase}</td>
                            <td className="p-2 text-center border">{job.type}</td>
                            <td className="p-2 text-center border w-[20%]">{job.job_id}</td>
                            <td className="p-2 text-center border w-[20%]">{job.label}</td>
                            <td className="p-2 text-center border">
                                {getDateTime(job.created_at)}
                            </td>
                            <td className="p-2 text-center border">
                                {getDateTime(job.started_at)}
                            </td>
                            <td className="p-2 text-center border w-[10%]">
                                {getDateTime(job.ended_at)}
                            </td>
                            <td className="p-2 text-center border w-[10%]">
                                {job.execution_duration ? `${Math.round(job.execution_duration * 100) / 100} sec` : ""}
                            </td>
                            <td className="p-2 text-center border w-[5%]">
                                <BlueButton onClick={() => handleView(job)}>
                                    View
                                </BlueButton>
                            </td>
                        </tr>
                    ))
                }
                </tbody>
            </table>
        </div>
    );
};

export default JobsTable;