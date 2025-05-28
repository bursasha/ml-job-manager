import React from 'react';
import Labelling from "../../../types/labelling.ts";
import spectrumSet from "../../../types/enums/spectrumSet.ts";

interface Props {
    labellings: Labelling[];
    currentInd: number;
    setCurrentInd: (currentInd: number) => void;
}

const Selector: React.FC<Props> = ({labellings, currentInd, setCurrentInd}) => {
    const getBgColor = (setName: string) => {
        if(setName === spectrumSet.PERFORMANCE_ESTIMATION)
            return "bg-orange-400"
        if(setName === spectrumSet.CANDIDATE)
            return "bg-blue-400"

        return "bg-gray-400"
    }

    const getBgHoverColor = (setName: string) => {
        if(setName === spectrumSet.PERFORMANCE_ESTIMATION)
            return "bg-orange-200 bg hover:bg-orange-600"
        if(setName === spectrumSet.CANDIDATE)
            return "bg-blue-200 hover:bg-blue-600"

        return "bg-gray-200  hover:bg-gray-600"
    }

    return (
        <div>
            <div className="p-2 space-y-1 h-[200px] overflow-y-auto border">
                {labellings.map((l, i) => (
                    <div
                        key={i}
                        onClick={() => setCurrentInd(i)}
                        className={`cursor-pointer p-2 rounded ${
                            i === currentInd ? getBgColor(l.spectrum_set) : getBgHoverColor(l.spectrum_set)
                        }`}
                    >
                        {l.spectrum_filename}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Selector;