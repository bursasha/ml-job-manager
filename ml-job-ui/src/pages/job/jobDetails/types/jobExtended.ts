import Job from "../../types/job.ts";

export default interface JobExtended extends Job {
    description: string,
    dir_path: string,
}