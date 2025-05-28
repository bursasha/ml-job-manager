import { Link } from 'react-router-dom';

import JobsView from "./components/jobsView/JobsView.tsx";
import BlueButton from "../../../components/buttons/BlueButton.tsx";

const JobList = () => {
    return (
        <div className="p-2">
            <div>
                <h2 className="text-xl font-bold mb-2">Create Jobs:</h2>
                <div className="flex space-x-2 mb-4">
                    <Link to={"/jobs/create/active_learning"}>
                        <BlueButton>
                            Active Learning
                        </BlueButton>
                    </Link>
                    <Link to={"/jobs/create/preprocessing"}>
                        <BlueButton>
                            Preprocessing
                        </BlueButton>
                    </Link>
                </div>
            </div>
            <div className="py-2">
                <JobsView/>
            </div>
        </div>
    );
};

export default JobList;