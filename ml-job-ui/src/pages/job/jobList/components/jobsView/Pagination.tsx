import React, {useEffect, useState} from 'react';
import BlueButton from "../../../../../components/buttons/BlueButton.tsx";

interface PaginationProps {
    items: number;
    totalCount: number;
    onPageChange: (page: number) => void;
    currentPage: number;
}

const Pagination: React.FC<PaginationProps> = ({items, totalCount, onPageChange, currentPage}) => {
    const [pages, setPages] = useState<number[]>([])
    const totalPages = Math.ceil(totalCount / items);
    const MAX_PAGES = 10;

    useEffect(() => {
        let start = Math.max(1, currentPage - Math.floor(MAX_PAGES / 2));
        let end = start + MAX_PAGES - 1;

        if (end > totalPages) {
            end = totalPages;
            start = Math.max(1, totalPages - MAX_PAGES + 1);
        }

        const temp = []
        for (let page = start; page <= end; page++) {
            temp.push(page);
        }
        setPages(temp)
    }, [currentPage, totalPages]);


    const handlePageChange = (page: number) => {
        console.log("total", totalPages);
        if (page < 1 || page > totalPages)
            return;
        onPageChange(page);
    };

    return (
        <div className="flex justify-center space-x-1 mt-3">
            <BlueButton onClick={() => handlePageChange(currentPage - 1)}
                        disabled={currentPage === 1}
            >
                Prev
            </BlueButton>

            {pages[0] > 1 && (
                <div>
                    <button onClick={() => handlePageChange(1)}
                            className="p-2 bg-gray-200 rounded cursor-pointer hover:bg-gray-300">1</button>
                    <span className="px-2">…</span>
                </div>
            )}

            {pages.map(page => (
                <button
                    key={page}
                    onClick={() => handlePageChange(page)}
                    disabled={page === currentPage}
                    className={`p-2 rounded cursor-pointer 
                        ${page === currentPage ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
                >
                    {page}
                </button>
            ))}

            {pages[pages.length - 1] < totalPages && (
                <div>
                    <span className="px-2">…</span>
                    <button onClick={() => handlePageChange(totalPages)}
                            className="p-2 bg-gray-200 rounded cursor-pointer hover:bg-gray-300">{totalPages}</button>
                </div>
            )}

            <BlueButton onClick={() => handlePageChange(currentPage + 1)}
                        disabled={currentPage === totalPages}
            >
                Next
            </BlueButton>
        </div>
    );
};

export default Pagination;