import React, {ChangeEvent} from 'react';

interface LabelFormProps {
    label: string;
    handleInputChange: (param: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
}

const LabelInput: React.FC<LabelFormProps> = ({label, handleInputChange}) => {
    return (
        <div>
            <label htmlFor="label" className="block text-gray-700 font-semibold mb-2">
                Label <span className="text-red-500">*</span>
            </label>
            <input
                id="label"
                name="label"
                type="text"
                value={label}
                onChange={(e) => handleInputChange(e)}
                required
                placeholder="Enter job label"
                className="w-full px-3 py-2  border rounded focus:outline-none focus:ring focus:border-black-500"
            />
        </div>
    );
};

export default LabelInput;