import React, {useState} from "react";

import {JobCreateDto} from "../types/jobCreateDto.ts";
import {useNavigate} from "react-router-dom";
import config from "../../../../config.ts";
import JobType from "../../types/enums/jobType.ts";

export const useJobForm = (jobType: JobType, jobViewUrl: string, checkFields: (config: object) => boolean) => {
    const navigate = useNavigate();
    const [jobDto, setJobDto] = useState<JobCreateDto>({
        label:"",
        description:"",
        type: jobType,
    });

    const [configText, setConfigText] = useState("");
    const [error, setError] = useState("");

    const sendConfigFile = async (jobConfig: object, dir_path: string) => {
        const temp = encodeURIComponent(dir_path)
        const blob = new Blob([JSON.stringify(jobConfig, null, 4)], { type: "application/json" });
        const formData = new FormData();
        formData.append("file", blob, "config.json");
        const response = await fetch(
            `${config.baseFileApi}/config.json/upload?parent_dir_path=${temp}`,
            {
                method: "POST",
                body: formData
            });

        if(!response.ok) {
            throw new Error("Error in config file creation: " + response.statusText);
        }
    }

    const sendJobCreateDto = async (jobCreateDto: JobCreateDto) => {
        if(!jobCreateDto.description) {
            delete jobCreateDto.description;
        }

        const response = await fetch(config.baseJobApi, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(jobCreateDto),
        });

        if (!response.ok) {
            console.error("Error in job creation sending: " + response.statusText);
            throw new Error(response.statusText);
        }
        return await response.json()
    }

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const {name, value} = e.target;
        // console.log(name, value)
        setJobDto(prev => ({ ...prev, [name]: value }));
    }

    const handleConfigTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => setConfigText(e.target.value);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        try {
            const fileReader = new FileReader();
            if(e.target.files) {
                fileReader.readAsText(e.target.files[0]);
                fileReader.onload = (event) => {
                    if(event.target)
                        setConfigText(String(event.target.result))
                }
            }
        }
        catch (err: unknown) {
            setError(err instanceof Error ? err.message: "Unknown error in config uploading");
        }
        finally {
            e.target.value = ""
        }
    }

    const handleLoadExampleConfig = async () => {
        try {
            const configObj = {
                [JobType.DATA_PREPROCESSING]: "/configs/prep_config.json",
                [JobType.ACTIVE_ML]: "/configs/al_config.json",
            }

            const response = await fetch(configObj[jobType])
            if(!response.ok) {
                throw new Error("Error in fetching example config: " + response.statusText);
            }
            setConfigText(await response.text())
        }
        catch (err: unknown) {
            setError(err instanceof Error ? err.message: "Unknown error in example config uploading");
        }

    }

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        setError("")
        try {
            if(!jobDto.label.trim())
                throw new Error("Label is required");
            const configJson = JSON.parse(configText)
            if(!configJson || typeof configJson !== 'object')
                throw new Error('Configuration is required');

            if(!checkFields(configJson))
                throw new Error("Missing required fields in configuration");

            const job = await sendJobCreateDto(jobDto);
            await sendConfigFile(configJson, job.dir_path);

            navigate(`${jobViewUrl}/${job.job_id}`)

        } catch (err) {
            setError(err instanceof Error ? err.message : "Unknown error in job creation");
        }
    };

    return {
        jobDto,
        error,
        configText,
        handleInputChange,
        handleConfigTextChange,
        handleFileChange,
        handleSubmit,
        handleLoadExampleConfig
    };
}
