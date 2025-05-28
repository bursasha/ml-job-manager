import {useCallback, useEffect, useState} from 'react';

import config from "../../../../../config.ts";
import Pagination from "./Pagination.tsx";
import Job from "../../../types/job.ts";
import JobPhase from "../../../types/enums/jobPhase.ts";
import JobsTable from "./JobsTable.tsx";

const LIMIT = 10;

const JobsView = () => {
    const [jobs, setJobs] = useState<Job[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    const [offset, setOffset] = useState(0);
    const [totalCount, setTotalCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(1);

    const fetchJobs = useCallback(async () => {
        try {
            setLoading(true)
            setError(false);
            const url = new URL(config.baseJobApi);
            url.searchParams.set("offset", offset.toString());
            url.searchParams.set("limit", LIMIT.toString());
            const response = await fetch(url.toString(), { method: "GET" });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            setJobs(data.jobs);
            setTotalCount(data.total);
        } catch (error) {
            console.error("Unknown error in jobs fetching: ", error);
            setError(true);
        } finally {
            setLoading(false);
        }
    },[offset]);

    useEffect(() => {
        fetchJobs();
    }, [fetchJobs]);

    useEffect(() => {
        if (jobs.some(job => job.phase === JobPhase.PROCESSING)) {
            console.log("hello")
            const timer = setTimeout(() => {
                fetchJobs()
            }, 10000);

            return () => clearTimeout(timer);
        }
    }, [fetchJobs, jobs]);


    const handlePageChange = (page: number) => {
        setCurrentPage(page);
        setOffset((page - 1) * LIMIT);
    };

    if(loading) return <div>Loading jobs...</div>;
    if(error) return <div>Error displaying jobs</div>;
    if(jobs.length === 0) return <div>No jobs to display...</div>;

    return (
        <div className="overflow-x-auto">
            <JobsTable jobs={jobs}/>
            <Pagination items={LIMIT} totalCount={totalCount}
                        onPageChange={handlePageChange} currentPage={currentPage}
            />
        </div>
    );
};

export default JobsView;