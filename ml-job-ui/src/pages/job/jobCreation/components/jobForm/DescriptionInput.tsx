import React, {ChangeEvent} from 'react';

interface DescFormProps {
    description: string | undefined;
    handleInputChange: (param: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
    error: string
}

const DescriptionInput: React.FC<DescFormProps> = ({description, handleInputChange}) => {
    return (
        <div>
            <label htmlFor="description" className="block text-gray-700 font-semibold mb-2">
                Description
            </label>
            <textarea
                id="description"
                name="description"
                value={description}
                onChange={(e) => handleInputChange(e)}
                placeholder="Enter job description (optional)"
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-black-500"
            />
        </div>
    );
};

export default DescriptionInput;