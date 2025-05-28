import JobPhase from "./enums/jobPhase.ts";
import JobType from "./enums/jobType.ts";

export default interface Job {
    phase: JobPhase;
    type: JobType;
    job_id: string;
    label: string;
    created_at: string;
    started_at: string;
    ended_at: string;
    execution_duration: number;
}
