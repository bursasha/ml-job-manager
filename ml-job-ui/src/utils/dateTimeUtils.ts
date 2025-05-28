const formatDateTime = (timeStr: string) => {
    return new Date(timeStr).toLocaleString();
}

export { formatDateTime };