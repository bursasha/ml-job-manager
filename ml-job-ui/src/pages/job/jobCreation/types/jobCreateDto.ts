import JobType from "../../types/enums/jobType.ts";

export interface JobCreateDto {
    type: JobType;
    label: string;
    description?: string;
}

