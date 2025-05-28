import React from "react";

import FitsSpectrum from "../../../types/fitsSpectrum.ts";

interface Props {
    metaData: FitsSpectrum;
}

const FitsMetadata: React.FC<Props> = ({metaData}) => {
    const toShow = Object.entries(metaData).filter(([key]) => key !== "wave" && key !== "flux");
    return (
        <div className="pl-17 w-[40%]">
            <table className="table-auto min-w-full border-collapse">
                <thead>
                <tr>
                    <th className="py-2 bg-gray-300 border">Name</th>
                    <th className="py-2 bg-gray-300 border">Value</th>
                </tr>
                </thead>
                <tbody>
                {
                    toShow.map(([key,value]) => (
                        <tr key={key}>
                            <td className="p-1 text-center border">{key}</td>
                            <td className="p-1 text-center border">{value}</td>
                        </tr>
                    ))
                }
                </tbody>
            </table>
        </div>
);
};

export default FitsMetadata;