import spectrumSet from "./enums/spectrumSet.ts";

export default interface Labelling {
    labelling_id: string;
    job_id: string;
    spectrum_filename: string;
    spectrum_set: spectrumSet;
    sequence_iteration: number;
    model_prediction: string;
    user_label: string | null;
    user_comment: string | null;
}