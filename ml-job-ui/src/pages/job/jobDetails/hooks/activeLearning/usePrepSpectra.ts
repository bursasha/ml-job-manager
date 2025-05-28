import {useEffect, useState} from "react";
import JobExtended from "../../types/jobExtended.ts";
import JobPhase from "../../../types/enums/jobPhase.ts";
import config from "../../../../../config.ts";

const usePrepSpectra = (job: JobExtended) => {
    const [waves, setWaves] = useState<number[]>([])
    const [spectra, setSpectra] = useState<Record<string, number[]>>({})
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("");
    useEffect(() => {
        const fetchSpectra = async () => {
            if(job.phase !== JobPhase.COMPLETED)
                return

            try {
                const dirPathQuery = encodeURIComponent(job.dir_path)
                const response = await fetch(`
                ${config.baseFileApi}/prep_spectra.json/download/?parent_dir_path=${dirPathQuery}`,
                    {method: "GET",}
                );

                if(!response.ok)
                    throw new Error("Error in fetching prep spectra: " + response.statusText);

                const data = await response.json();
                setWaves(data.wave);
                setSpectra(data.spectra);
            } catch (err) {
                setError(err instanceof Error ? err.message : "Unknown error in fetch prep spectra");
            }
            finally {
                setLoading(false);
            }

        }

        fetchSpectra()
    }, [job])


    return { waves, spectra, loading, error };
}

export default usePrepSpectra;