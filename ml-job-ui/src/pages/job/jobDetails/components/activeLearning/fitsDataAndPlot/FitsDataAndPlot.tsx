import React, {useEffect, useState} from 'react';
import useFitsSpectrum from "../../../hooks/activeLearning/useFitsSpectrum.ts";
import BlueButton from "../../../../../../components/buttons/BlueButton.tsx";
import SpectrumPlot from "../SpectrumPlot.tsx";
import FitsMetadata from "./FitsMetadata.tsx";

interface Props {
    filename: string;
}

const FitsDataAndPlot: React.FC<Props> = ({filename}) => {
    const { fitsSpectrum, loading, error, fetchFits } = useFitsSpectrum(filename);
    const [show, setShow] = useState(false);

    const handleClick = async () => {
        if(!fitsSpectrum)
            await fetchFits();

        setShow(prev => !prev);
    }

    useEffect(() => {
        setShow(false);
    },[filename])

    return (
        <div>
            <div className="mb-4">
                <BlueButton onClick={handleClick}>
                    {show ? "Hide" : "Show"} raw data
                </BlueButton>
            </div>
            {
                show && (
                    <>
                        {
                            loading ? (<p>Loading FITS data</p>)
                                : error ? (<p className="text-red-800">{error}</p>)
                                : fitsSpectrum && (
                                    <div  className="space-y-3">
                                        <SpectrumPlot title="Raw Plot" waves={fitsSpectrum.wave}
                                                      fluxes={fitsSpectrum.flux}/>
                                        <FitsMetadata metaData={fitsSpectrum}/>
                                    </div>
                                )
                        }
                    </>
                )
            }
        </div>
    );
};

export default FitsDataAndPlot;