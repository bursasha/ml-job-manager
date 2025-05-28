import React from 'react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
    return (
        <nav className="flex p-4 space-x-5 bg-indigo-400">
            <h1 className="text-white text-xl font-bold">
                ML Job Manager
            </h1>
            <div className="flex space-x-5 mt-0.5">
                <Link to="/" className="text-gray-300 hover:text-white">
                    Home
                </Link>
                <Link to="/jobs" className="text-gray-300 hover:text-white">
                    Jobs
                </Link>
                <Link to={`/fileSystem/?path=${encodeURIComponent("/")}`} className="text-gray-300 hover:text-white">
                    Filesystem
                </Link>
            </div>
        </nav>
    );
};

export default Navbar;
