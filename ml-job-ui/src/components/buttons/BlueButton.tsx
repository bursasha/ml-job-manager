import React, {ButtonHTMLAttributes} from 'react';

interface Props extends ButtonHTMLAttributes<HTMLButtonElement>{
    children: React.ReactNode;
}

const BlueButton: React.FC<Props> = ({children, ...props}) => {
    return (
        <div>
            <button {...props} type="button"
                    className="p-2 bg-blue-600 text-white rounded
                               cursor-pointer disabled:opacity-50 hover:bg-blue-800"
            >
                {children}
            </button>
        </div>
    );
};

export default BlueButton;