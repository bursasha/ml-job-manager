// if(!import.meta.env.VITE_BASE_API_JOB) {
//     throw new Error("BASE_JOB_API is required");
// }

const API_URL = import.meta.env.VITE_API_URL as string;

const config = {
    baseJobApi: `${API_URL}/jobs`,
    baseFileApi: `${API_URL}/files`,
    baseLabellingApi: `${API_URL}/labellings`,
    baseSpectraApi: `${API_URL}/spectra`,
};

export default config;