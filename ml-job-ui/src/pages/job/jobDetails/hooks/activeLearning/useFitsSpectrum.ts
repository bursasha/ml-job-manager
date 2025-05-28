import {useEffect, useState} from "react";
import FitsSpectrum from "../../types/fitsSpectrum.ts";
import config from "../../../../../config.ts";

const useFitsSpectrum = (filename: string) => {
    const [fitsSpectrum, setFitsSpectrum] = useState<FitsSpectrum | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const fetchFits = async () => {
        if(!filename)
            return;

        setLoading(true);
        setError("");
        try {
            const response = await fetch(`${config.baseSpectraApi}/${filename}`, { method: "GET"});
            if (!response.ok) {
                throw new Error("Error in fits spectrum fetching: " + response.statusText);
            }
            const data = await response.json();
            setFitsSpectrum(data);
        }
        catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Unknown error in fits fetching");
        }
        finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        setFitsSpectrum(null);
    },[filename])


    return {fitsSpectrum, loading, error, fetchFits};
}

export default useFitsSpectrum;