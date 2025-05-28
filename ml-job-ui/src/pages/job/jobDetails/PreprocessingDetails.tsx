import {useParams} from "react-router-dom";
import useJobExtended from "./hooks/useJobExtended.ts";
import JobData from "./components/JobData.tsx";
import JobFiles from "./components/JobFiles.tsx";
import useJobFiles from "./hooks/useJobFiles.ts";

const PreprocessingDetails = () => {
    const { jobId } = useParams();
    const {job, setJob , loading, error} = useJobExtended(jobId)
    const { files, loading: filesLoading, error: filesError } = useJobFiles(job);

    if(loading) return <p>Loading job...</p>;
    if(error) return <p>Error in job fetching: {error}</p>;

    return (
        <div className="space-y-5">
            <JobData job={job} setJob={setJob} />
            <JobFiles job={job} files={files} loading={filesLoading} error={filesError}
            />
        </div>
    );
};

export default PreprocessingDetails;