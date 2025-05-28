import React, {ChangeEvent} from 'react';
import BlueButton from "../../../../../components/buttons/BlueButton.tsx";

interface ConfigFromProps {
    configText: string;
    handleConfigTextChange: (e: ChangeEvent<HTMLTextAreaElement>) => void;
    handleFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    handleLoadExampleConfig: () => void;
}

const ConfigInput: React.FC<ConfigFromProps> = ({configText,
                                                    handleConfigTextChange,
                                                    handleFileChange,
                                                    handleLoadExampleConfig}) =>
{
    return (
        <div>
            <label htmlFor="configuration" className="block text-gray-700 font-semibold mb-2">
                Configuration
            </label>
            <textarea
                id="configuration"
                name="configuration"
                value={configText}
                required
                onChange={(e) => handleConfigTextChange(e)}
                placeholder="Enter configuration manually or upload JSON file"
                className="w-full h-50 px-3 py-2 border rounded
                            focus:outline-none focus:ring focus:border-black-500"
            />
            <div className="mt-5">
                <input id="fileUpload" type="file" hidden onChange={handleFileChange}/>
                <label htmlFor="fileUpload" className="p-2 bg-blue-600 text-white rounded
                               cursor-pointer disabled:opacity-50 hover:bg-blue-800"
                >
                    Upload file
                </label>
                <div className="mt-5">
                    <BlueButton onClick={handleLoadExampleConfig}>
                        Upload example config
                    </BlueButton>
                </div>
            </div>
        </div>
    );
};

export default ConfigInput;