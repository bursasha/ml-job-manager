interface FileEntry {
    filename: string;
    size: number | null;
    modified_at: string | null;
}

export default FileEntry;