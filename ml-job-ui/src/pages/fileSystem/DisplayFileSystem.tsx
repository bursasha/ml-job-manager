import React from "react";

import useFileSystem from "./hooks/useFileSystem.ts";
import {Link, useSearchParams} from "react-router-dom";
import useFileSystemActions from "./hooks/useFileSystemActions.ts";
import BlueButton from "../../components/buttons/BlueButton.tsx";
import {formatDateTime} from "../../utils/dateTimeUtils.ts";

const DisplayFileSystem = () => {
    const [searchParams] = useSearchParams();
    const path = searchParams.get('path') ?? "";

    const {files, setFiles, directories, setDirectories, loading, error} = useFileSystem(path);
    const {
        handleFileDownload,
        handleFileDeletion,
        handleDirDeletion,
        handleFileUpload,
        handleDirCreation,
        errorMsg,
        successMsg,
        clearMsgs
    } = useFileSystemActions(path)

    const handleFileDeletionExtended = async (filename: string) => {
        if(await handleFileDeletion(filename)) {
            setFiles(prev => prev.filter(f => f.filename !== filename));
        }
    }

    const handleDirDeletionExtended = async (dirname: string) => {
        if(await handleDirDeletion(dirname)) {
            setDirectories(prev => prev.filter(d => d !== dirname));
        }
    }

    const handleFileUploadExtended = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const data = await handleFileUpload(e);
        e.target.value = ""
        if(data) {
            setFiles(prev => [...prev, data]);
            console.log(data)
        }
    }

    const handleDirCreationExtended = async () => {
        const data = await handleDirCreation(directories)
        if(data)
            setDirectories(prev => [...prev, data.dirname]);
    }

    const handleLinkRedirect = (dirname: string) => {
        let new_path = path;
        if(new_path !== "/")
            new_path += "/";
        new_path += dirname;
        return "/filesystem/?path=" + encodeURIComponent(new_path)
    }

    if(loading) return <p>Loading filesystem</p>
    if(error) return <p>Error loading filesystem.</p>
    return (
        <div className={"mt-8"}>
            <div className="mb-5">
                {
                    (successMsg || errorMsg) &&
                    <div className="flex space-x-5 mb">
                        <p className={`${ successMsg ? "text-green-800" : "text-red-800"}`}>
                            {successMsg || errorMsg}
                        </p>
                        <button className="cursor-pointer flex justify-center items-center
                                            w-5 h-5 bg-gray-400 hover:bg-gray-500 rounded mt-1 pb-1"
                                onClick={clearMsgs}>
                            x
                        </button>
                    </div>
                }
            </div>
            <div className="flex items-center space-x-2 mb-4">
                <div>
                    <input id="fileUpload" type="file" hidden onChange={handleFileUploadExtended} />
                    <label htmlFor="fileUpload" className="p-2 bg-blue-600 text-white rounded
                               cursor-pointer disabled:opacity-50 hover:bg-blue-800 inline-block"
                    >
                        Upload file
                    </label>
                </div>
                <BlueButton onClick={handleDirCreationExtended}>
                    Create new directory
                </BlueButton>
            </div>
            <p className="mb-4">Directory: {decodeURIComponent(path)}</p>
            <table className="table-auto min-w-full border-collapse">
                <thead>
                <tr>
                    <td className="p-2 text-center border">Name</td>
                    <td className="p-2 text-center border">Size</td>
                    <td className="p-2 text-center border">Last modified</td>
                    <td className="p-2 text-center border">Download</td>
                    <td className="p-2 text-center border">Delete</td>
                </tr>
                </thead>
                <tbody>
                {
                    files.map((f) => (
                        <tr key={f.filename}>
                            <td className="p-2 border w-[30%]">
                                {f.filename}
                            </td>
                            <td className="p-2 text-center border">
                                {f.size} B
                            </td>
                            <td className="p-2 text-center border w-[15%]">
                                {f.modified_at ? formatDateTime(f.modified_at) : ""}
                            </td>
                            <td className="p-2 text-center border w-[10%]">
                                <button className="px-2 bg-blue-600 text-white rounded
                                        cursor-pointer disabled:opacity-50 hover:bg-blue-800"
                                        onClick={() => handleFileDownload(f.filename)}
                                >
                                    Download
                                </button>
                            </td>
                            <td className="p-2 text-center border w-[10%]">
                                <button
                                    onClick={() => handleFileDeletionExtended(f.filename)}
                                    className="px-2 rounded cursor-pointer bg-red-600
                                            text-white disabled:opacity-50 hover:bg-red-800"
                                >
                                    DELETE
                                </button>
                            </td>
                        </tr>
                    ))

                }

                {
                    directories.map((d, i) => (
                        <tr key={i + files.length}>
                            <td className="p-2 border w-[30%]">
                                <Link to={handleLinkRedirect(d)}>
                                    <p className="underline text-blue-500 hover:text-blue-900">{d}</p>
                                </Link>
                            </td>
                            <td className="p-2 text-center border">
                            </td>
                            <td className="p-2 text-center border w-[15%]">
                            </td>
                            <td className="p-2 text-center border w-[10%]">
                            </td>
                            <td className="p-2 text-center border w-[10%]">
                                <button
                                    onClick={() => handleDirDeletionExtended(d)}
                                    className="px-2 rounded cursor-pointer bg-red-600
                                            text-white disabled:opacity-50 hover:bg-red-800"
                                >
                                    DELETE
                                </button>
                            </td>
                        </tr>
                    ))
                }
                </tbody>
            </table>
        </div>
    );
};

export default DisplayFileSystem;