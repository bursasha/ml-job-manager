import JobForm from "./components/jobForm/JobForm.tsx";
import jobType from "../types/enums/jobType.ts";

const ActiveLearningCreation = () => {
    const validateConfig = (config: object) => {
        const fields = ["pool_data_path", "classes", "candidate_classes", "iteration"];
        const training_data = "training_data_path";
        const tr_data_to_add = "training_data_to_add_path";
        const oracle_data = "oracle_data_to_add_path";
        for (const f of fields) {
            if (!(f in config)) {
                return false;
            }
        }

        if("iteration" in config && config["iteration"] != 0) {
            if(!(training_data in config) && !(tr_data_to_add in config && oracle_data in config)) {
                return false;
            }
        }
        return true;
    }

    return (
        <div>
            <h1 className="text-3xl font-bold mb-4">Create Active Learning Job</h1>
            <JobForm type={jobType.ACTIVE_ML} jobDetailsUrl={"/jobs/details/active_learning"}
                checkFields={validateConfig}/>
        </div>
    );
};

export default ActiveLearningCreation;