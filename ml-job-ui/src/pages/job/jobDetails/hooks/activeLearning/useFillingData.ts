import Labelling from "../../types/labelling.ts";
import {Dispatch, SetStateAction, useEffect, useRef, useState} from "react";
import config from "../../../../../config.ts";
import spectrumSet from "../../types/enums/spectrumSet.ts";

const useFillingData = (labellings: Labelling[],
                        setLabellings: Dispatch<SetStateAction<Labelling[]>>,
                        setCurrentInd: Dispatch<SetStateAction<number>>) =>
{
    const [submitError, setSubmitError] = useState("");
    const [submitSuccess, setSubmitSuccess] = useState("");

    const [labellingStats, setLabellingStats] = useState(
        {
            oracleSpectraCnt: 0,
            perfEstSpectraCnt: 0,
            labelledOracleCnt: 0,
            labelledPerfEstCnt: 0
        }
    );

    const clearSubmitMsgs = () => {
        setSubmitError("");
        setSubmitSuccess("");
    }

    useEffect(() => {
        const oracleSpectra = labellings.filter(l => l.spectrum_set === "ORACLE");
        const perfEstSpectra = labellings.filter(l => l.spectrum_set === "PERFORMANCE_ESTIMATION");
        const labelledOracleCnt = oracleSpectra.filter(l => l.user_label).length;
        const labelledPerfEstCnt = perfEstSpectra.filter(l => l.user_label).length
        console.log(labelledPerfEstCnt)
        setLabellingStats({
            oracleSpectraCnt: oracleSpectra.length,
            perfEstSpectraCnt: perfEstSpectra.length,
            labelledOracleCnt: labelledOracleCnt,
            labelledPerfEstCnt: labelledPerfEstCnt
        });
    }, [labellings]);

    const [selections, setSelections] = useState<string[]>(
        new Array(labellings.length).fill("")
    );

    const [comments, setComments] = useState<string[]>(
        new Array(labellings.length).fill("")
    );

    const changedIndexes = useRef<Set<number>>(new Set());

    const sendOracleData = async (newLabellings: Labelling[], classes: string[], dir_path: string) => {
        if(!newLabellings.length)
            return;

        const classesIndexes = Object.fromEntries(classes.map((c, i) => [c, i]))
        const filenames = [];
        const labels = [];
        for(const l of newLabellings) {
            if(l.user_label) {
                filenames.push(l.spectrum_filename);
                labels.push(classesIndexes[l.user_label]);
            }
        }
        const oracleData = {
            filenames: filenames,
            labels: labels
        }

        const encodedPath = encodeURIComponent(dir_path)
        const blob = new Blob([JSON.stringify(oracleData)], { type: "application/json" });
        const formData = new FormData();
        formData.append("file", blob, "oracle_data.json");
        const response = await fetch(
            `${config.baseFileApi}/oracle_data.json/upload?parent_dir_path=${encodedPath}`,
            {
                method: "POST",
                body: formData
            });
        if(!response.ok)
            throw new Error("Failed to create oracle_data.json: " + response.statusText);
    }

    const sendPerfEstData = async (newLabellings: Labelling[], dirPath: string, iteration: number | null) => {
        if(iteration === null)
            throw new Error("Iteration not provided for performances estimation labellings");
        if(!newLabellings.length)
            return;
        let totalCnt = 0;
        let correctCnt = 0;

        for(const l of newLabellings) {
            if(l.user_label) {
                ++totalCnt;
                if(l.user_label === l.model_prediction){
                    ++correctCnt;
                }
            }
        }

        if(totalCnt !== newLabellings.length)
            return;

        const encodedPath = encodeURIComponent(dirPath)
        const responseGet = await fetch(`
                ${config.baseFileApi}/perf_est_list.json/download/?parent_dir_path=${encodedPath}`,
            {method: "GET",}
        );

        if(!responseGet.ok)
            throw new Error("Error in fetching perf_est_list.json: " + responseGet.statusText);

        const perfEstArr: number[] = await responseGet.json();
        if(perfEstArr.length === iteration) {
            perfEstArr[perfEstArr.length - 1] = correctCnt / totalCnt;
        }
        else {
            perfEstArr.push(correctCnt / totalCnt);
        }

        const blob = new Blob([JSON.stringify(perfEstArr)], { type: "application/json" });
        const formData = new FormData();
        formData.append("file", blob, "perf_est_list");
        const responsePost = await fetch(
            `${config.baseFileApi}/perf_est_list.json/upload?parent_dir_path=${encodedPath}`,
            {
                method: "POST",
                body: formData
            });
        if(!responsePost.ok)
            throw new Error("Failed to create perf_est_list.json: " + responsePost.statusText);
    }

    const submitLabellings = async (classes: string[], dirPath: string, updateFiles: () => void, iteration: number | null) => {
        setSubmitError("")
        setSubmitSuccess("")
        if(changedIndexes.current.size === 0)
            return;

        const ids: string[] = [];
        const changes: Record<string, string>[] = []
        const mapChangedLabellings = new Map<string, Labelling>()
        for(const ind of changedIndexes.current) {
            const temp: Record<string, string> = {}
            if(selections[ind])
                temp.user_label = selections[ind]
            if(comments[ind])
                temp.user_comment = comments[ind]

            if(Object.keys(temp).length > 0) {
                ids.push(labellings[ind].labelling_id);
                changes.push(temp);
                mapChangedLabellings.set(labellings[ind].labelling_id, {...labellings[ind], ...temp});
            }
        }

        try {
            const response = await fetch(`${config.baseLabellingApi}/batch/`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    "labelling_ids": ids,
                    "batch": changes,
                })
            })

            if(!response.ok) {
                throw new Error("Error in submitting labels and comments: " + response.statusText);
            }

            const new_labellings = labellings.map(l => mapChangedLabellings.get(l.labelling_id) ?? l)
            setLabellings(new_labellings);
            changedIndexes.current.clear();
            setSelections(new Array(new_labellings.length).fill(""));
            setComments(new Array(new_labellings.length).fill(""));
            await sendOracleData(new_labellings.filter(l => l.spectrum_set === spectrumSet.ORACLE ), classes, dirPath);
            if(iteration !== 0) {
                await sendPerfEstData(new_labellings.filter(l =>
                        l.spectrum_set === spectrumSet.PERFORMANCE_ESTIMATION), dirPath, iteration
                );
            }
            updateFiles();
            setSubmitSuccess("Labels and comments were saved")
        }
        catch (err: unknown) {
            setSubmitError(err instanceof Error ?
                err.message
                : "Unknown error in labelling submitting"
            );
        }

    };

    const handleRadioChange = (specIndex: number, value: string) => {
        if(specIndex !== labellings.length - 1)
            setCurrentInd(specIndex + 1);
        setSelections((prev) => {
            const updated = [...prev];
            updated[specIndex] = value;
            changedIndexes.current.add(specIndex);
            return updated;
        });
    };

    const handleCommentChange = (specIndex: number, value: string) => {
        setComments(prev => {
            const updated = [...prev];
            updated[specIndex] = value;
            changedIndexes.current.add(specIndex);
            if(!value)
                changedIndexes.current.delete(specIndex);
            return updated;
        });
    };


    return { selections, comments, labellingStats,
        submitLabellings, handleRadioChange, handleCommentChange,
        submitSuccess, submitError, clearSubmitMsgs };
}

export default useFillingData;