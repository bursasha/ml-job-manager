import JobForm from "./components/jobForm/JobForm.tsx";
import jobType from "../types/enums/jobType.ts";

const PreprocessingCreation = () => {
    const validateConfig = (config: object) => {
        const fields = ["wave_start_point", "wave_end_point", "wave_point_count", "data_dir_path"];
        for (const f of fields) {
            if (!(f in config)) {
                return false;
            }
        }
        return true;
    }

    return (
        <div>
            <h1 className="text-3xl font-bold mb-4">Create Preprocessing Job</h1>
            <JobForm type={jobType.DATA_PREPROCESSING} jobDetailsUrl={"/jobs/details/preprocessing"}
                        checkFields={validateConfig}/>
        </div>
    );
};

export default PreprocessingCreation;