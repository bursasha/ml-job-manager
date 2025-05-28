import React from 'react';
import {useJobForm} from "../../hooks/useJobForm.ts";
import LabelInput from "./Labelnput.tsx";
import DescriptionInput from "./DescriptionInput.tsx";
import ConfigInput from "./ConfigInput.tsx";
import JobType from "../../../types/enums/jobType.ts";

interface JobFormProps {
    type: JobType;
    jobDetailsUrl: string;
    checkFields: (config: object) => boolean;
}

const JobForm: React.FC<JobFormProps> = ({type, jobDetailsUrl, checkFields}) => {
    const {
        jobDto,
        error,
        configText,
        handleInputChange,
        handleConfigTextChange,
        handleFileChange,
        handleSubmit,
        handleLoadExampleConfig
    } = useJobForm(type, jobDetailsUrl, checkFields)

    return (
        <div>
            <div className="p-4 bg-white max-w-2xl rounded-md" >
                <form  onSubmit={handleSubmit}>
                    <h2 className="mb-3 font-bold text-xl">Form</h2>
                    {
                        error &&
                        <p className="text-red-800">{error}</p>
                    }
                    <div className="mb-4">
                        <LabelInput label={jobDto.label} handleInputChange={handleInputChange}
                                    />
                    </div>
                    <div className="mb-4">
                        <DescriptionInput description={jobDto.description}
                                          handleInputChange={handleInputChange} error={""} />
                    </div>
                    <div className="mb-4">
                        <ConfigInput configText={configText} handleConfigTextChange={handleConfigTextChange}
                                     handleFileChange={handleFileChange} handleLoadExampleConfig={handleLoadExampleConfig} />
                    </div>
                    <div className="flex justify-center">
                        <button
                            type="submit"
                            className="w-[70%] bg-blue-600 text-white py-2 rounded hover:bg-blue-700 cursor-pointer"
                        >
                            Submit
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default JobForm;