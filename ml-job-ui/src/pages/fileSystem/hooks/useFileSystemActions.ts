import React, {useState} from "react";
import config from "../../../config.ts";
import {saveAs} from 'file-saver'

const useFileSystemActions = (path: string) => {
    const [errorMsg, setErrorMsg] = useState("");
    const [successMsg, setSuccessMsg] = useState("");

    const clearMsgs = () => {
        setSuccessMsg("");
        setErrorMsg("");
    }

    const handleFileDownload = async (filename: string) => {
        clearMsgs();
        try {
            const pathEncoded = encodeURIComponent(path);
            const response = await fetch(`
                    ${config.baseFileApi}/${filename}/download/?parent_dir_path=${pathEncoded}`,
                {
                    method: "GET",
                });
            if(!response.ok) {
                throw new Error("Error in file downloading: " + response.statusText);
            }

            const blob = await response.blob();

            saveAs(blob, filename);
            return true;
        }
        catch (err: unknown){
            setErrorMsg(err instanceof Error ? err.message : `Unknown error downloading file: ${filename}`);
            return false;
        }
    }

    const handleFileDeletion = async (filename: string) => {
        clearMsgs();
        if(window.confirm(`Are you sure you want to delete file: ${filename}?`)) {
            const pathEncoded = encodeURIComponent(path);
            try {
                const response = await fetch(
                    `${config.baseFileApi}/${filename}/?parent_dir_path=${pathEncoded}`,
                    {
                        method: "DELETE",
                    })
                if (!response.ok) {
                    throw new Error("Error in file deletion. " +  response.statusText);
                }
                setSuccessMsg(`File ${filename} has been deleted`);
                return true;
            } catch (err: unknown) {
                setErrorMsg(err instanceof Error ? err.message : "Unknown error in file deletion");
                return false;
            }
        }
        return false;
    }

    const handleDirDeletion = async (dirName: string) => {
        clearMsgs();
        if(window.confirm(`Are you sure you want to delete directory: ${dirName}?`)) {
            try {
                const pathEncoded = encodeURIComponent(path);
                const response = await fetch(
                    `${config.baseFileApi}/directories/${dirName}/?parent_dir_path=${pathEncoded}`,
                    {
                        method: "DELETE",
                    })
                if (!response.ok) {
                    throw new Error("Error in directory deletion: " +  response.statusText);
                }

                setSuccessMsg(`Directory ${dirName} has been deleted`);
                return true;
            } catch (err: unknown) {
                setErrorMsg(err instanceof Error ? err.message : "Unknown error in directory deletion");
                return false;
            }
        }
        return false;
    }

    const handleFileUpload = async(e: React.ChangeEvent<HTMLInputElement>) => {
        clearMsgs();
        try {
            const file = e.target.files?.[0]
            if (!file) {
                throw new Error("File is required");
            }
            const formData = new FormData();
            formData.append("file", file, file.name);
            const pathEncoded = encodeURIComponent(path);
            const response =  await fetch(
                `${config.baseFileApi}/${file.name}/upload?parent_dir_path=${pathEncoded}`,
                {
                    method: "POST",
                    body: formData
            });

            if(!response.ok) {
                throw new Error("Error in file uploading: " + response.statusText);
            }
            const data = await response.json();
            setSuccessMsg("File has been uploaded");
            return data;
        }
        catch (err: unknown) {
            setErrorMsg(err instanceof Error ? err.message : "Unknown error in file uploading");
            return null;
        }
    }

    const handleDirCreation = async (dirNames: string[]) => {
        clearMsgs();
        try {
            const name = window.prompt("Enter directory name");
            if(!name) return;

            if(!name.trim())
                throw new Error("Directory name is empty")

            if(dirNames.includes(name))
                throw new Error(`Directory name ${name} already exists`);

            const pathEncoded = encodeURIComponent(path);
            const response = await fetch(
                `${config.baseFileApi}/directories/${encodeURIComponent(name)}/?parent_dir_path=${pathEncoded}`,
                { method: "POST"})

            if(!response.ok)
                throw new Error("Error in directory creation: " + response.statusText);

            const data = response.json();
            setSuccessMsg("Directory has been created")
            return data;
        }
        catch (err: unknown) {
            setErrorMsg(err instanceof Error ? err.message : "Unknown error in directory creation");
            return null;
        }

    }

    return {
        handleFileDownload,
        handleFileDeletion,
        handleDirDeletion,
        handleFileUpload,
        handleDirCreation,
        successMsg,
        errorMsg,
        clearMsgs
    }
}

export default useFileSystemActions;