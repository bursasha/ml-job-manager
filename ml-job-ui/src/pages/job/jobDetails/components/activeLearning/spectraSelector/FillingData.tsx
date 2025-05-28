import React, {Dispatch, SetStateAction} from 'react';
import BlueButton from "../../../../../../components/buttons/BlueButton.tsx";
import Labelling from "../../../types/labelling.ts";
import useFillingData from "../../../hooks/activeLearning/useFillingData.ts";
import useClasses from "../../../hooks/activeLearning/useClasses.ts";

interface Props {
    labellings: Labelling[];
    setLabellings: Dispatch<SetStateAction<Labelling[]>>
    currentInd: number;
    setCurrentInd: Dispatch<SetStateAction<number>>;
    dirPath: string;
    updateFiles: () => void;
    iteration: number | null;
}

// const classes = ["other", "single peak", "double peak"]

const FillingData: React.FC<Props> = ({   labellings, setLabellings,
                                          currentInd, setCurrentInd,
                                          dirPath, updateFiles, iteration
}) => {
    const {
        selections,
        comments,
        submitLabellings,
        handleRadioChange,
        handleCommentChange,
        labellingStats,
        submitError,
        submitSuccess,
        clearSubmitMsgs
    } = useFillingData(labellings, setLabellings, setCurrentInd);
    const {classes, error: classesError } = useClasses(dirPath)

    return (
        <div className="flex">
            <div className="mb-4">
            <h1 className="text-xl font-bold mb-2">Classification</h1>
                <div className="flex">
                    <div className="flex flex-col space-y-2">
                        {classesError && <p className="text-red-800">{classesError}</p>}
                        {!classesError && classes.map((item, index) => (
                            <label key={index} className="space-x-2">
                                <input
                                    type="radio"
                                    name={`radiobutton-${currentInd}`}
                                    value={item}
                                    checked={selections[currentInd] === item}
                                    onChange={() => handleRadioChange(currentInd, item)}
                                />
                                <span>{index + 1} - {item}</span>
                            </label>
                        ))}
                        <div className="flex space-x-4 mt-2">
                            <BlueButton onClick={() => setCurrentInd(currentInd - 1)}
                                        disabled={currentInd === 0}
                            >
                                Prev
                            </BlueButton>
                            <BlueButton onClick={() => setCurrentInd(currentInd + 1)}
                                        disabled={currentInd === labellings.length - 1}
                            >
                                Next
                            </BlueButton>
                        </div>
                    </div>
                    <div className="space-y-10 ml-15">
                        <input
                            type="text"
                            className="px-2 py-1 border rounded"
                            placeholder="Comment"
                            value={comments[currentInd]}
                            onChange={e => handleCommentChange(currentInd, e.target.value)}
                        />
                        <BlueButton onClick={() => submitLabellings(classes, dirPath, updateFiles, iteration)}>
                            Submit
                        </BlueButton>
                    </div>
                </div>
            </div>
            <div className="ml-5 space-x-2">
                {/*<p className="text-red-600 font-bold">Oracle labels is changed</p>*/}
                <p>
                    Oracle specter labeled: {labellingStats.labelledOracleCnt}/{labellingStats.oracleSpectraCnt}
                </p>
                <p>
                    Performance estimation specter labeled: {labellingStats.labelledPerfEstCnt}/{labellingStats.perfEstSpectraCnt}
                </p>
                <div className="mt-5">
                    {
                        (submitSuccess || submitError ) &&
                        <div className="flex space-x-5 mb">
                            <p className={`${ submitSuccess ? "text-green-800" : "text-red-800"}`}>
                                {submitSuccess || submitError}
                            </p>
                            <button className="cursor-pointer flex justify-center items-center
                                            w-5 h-5 bg-gray-400 hover:bg-gray-500 rounded mt-1 pb-1"
                                    onClick={clearSubmitMsgs}>
                                x
                            </button>
                        </div>
                    }
                </div>
            </div>
        </div>
    );
};

export default FillingData;