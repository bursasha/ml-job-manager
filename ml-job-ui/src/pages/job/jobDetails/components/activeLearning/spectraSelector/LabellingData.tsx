import React from 'react';
import Labelling from "../../../types/labelling.ts";

interface Props {
    labelling: Labelling
}

const LabellingData: React.FC<Props> = ({labelling}) => {
    return (
        <div>
            <table className="table-auto w-[90%]">
                <thead>
                    <tr>
                        <td className="p-2 bg-gray-300 text-center border">Filename</td>
                        <td className="p-2 bg-gray-300 text-center border">Set</td>
                        <td className="p-2 bg-gray-300 text-center border">Model prediction</td>
                        <td className="p-2 bg-gray-300 text-center border">User label</td>
                        <td className="p-2 bg-gray-300 text-center border">User comment</td>
                    </tr>
                </thead>
                <tbody>
                <tr>
                    <td className="p-2 text-center border w-[30%]">
                        {labelling.spectrum_filename}
                    </td>
                    <td className="p-2 text-center border w-[20%]">
                        {labelling.spectrum_set}
                    </td>
                    <td className="p-2 text-center border w-[15%]">
                        {labelling.model_prediction}
                    </td>
                    <td className="p-2 text-center border w-[15%]">
                        {labelling.user_label}
                    </td>
                    <td className="p-2 text-center border w-[20%]">
                        {labelling.user_comment}
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    );
};

export default LabellingData;