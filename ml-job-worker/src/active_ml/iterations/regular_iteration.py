import numpy as np
import json
from scipy.stats import entropy
from sklearn.manifold import TSNE
from numpy.typing import NDArray
from typing import Any

from src.active_ml.types import LabellingSpectrumSetType
from src.active_ml.config import ActiveLearningConfig
from src.active_ml import file_utils
from src.active_ml import cnn_model

def get_tr_data(config: ActiveLearningConfig
                ) -> tuple[NDArray[str], NDArray[float], NDArray[NDArray[float]], NDArray[int]]:
    """
    Reads training data from provided HDF5 file, and additional training data from HDF5 and JSON files.

    If HDF5 file for training data is provided, reads data from file.

    If HDF5 file for additinoal training data is provided:
        Reads from HDF5 file spectrum filenames, wave and fluxes.
        Reads spectrum filenames and labels from provided JSON file.
        Finds corresponding fluxes using filenames from JSON file.
        Concatenates all training data.
    
    After loading all training data, removes duplicates spectra using filenames.

    Parameters:
        config (ActiveLearningConfig): job's configuration, loaded from configuration file.

    Returns:
        Tuple[NDArray[str], NDArray[float], NDArray[NDArray[float]], NDArray[int]]:
            1D array of spectrum filenames.
            1D array of spectrum wave.
            2D array of spectrum fluxes.
            1D array of labels.
    """

    if config.training_data_path:
        filenames_tr, wave_tr, fluxes_tr, labels_tr = file_utils.read_training_data(config.training_data_path)
    else:
        filenames_tr, wave_tr, fluxes_tr, labels_tr = np.array([]), np.array([]) , np.array([]), np.array([], dtype=int)


    if config.training_data_to_add_path:
        filenames_to_add, wave_to_add, fluxes_to_add = file_utils.read_pool_data(config.training_data_to_add_path)
        if filenames_tr.shape[0] and not np.array_equal(wave_tr, wave_to_add):
            raise ValueError("Different waves in 'training data' and 'label to add'")
        
        with open(config.oracle_data_to_add_path) as f:
            oracle_data = json.load(f)

        filenames_oracle = np.array(oracle_data["filenames"])
        mask = np.isin(filenames_to_add, filenames_oracle)
        selected_filenames = filenames_to_add[mask]
        selected_fluxes = fluxes_to_add[mask]
        filename_fluxes = dict(zip(selected_filenames, selected_fluxes))
        fluxes_oracle = np.array([filename_fluxes[f_oracle] for f_oracle in filenames_oracle])

        filenames_tr = np.concatenate((filenames_tr, filenames_oracle))
        # fluxes_tr = np.concatenate((fluxes_tr, fluxes_oracle))
        labels_tr = np.concatenate((labels_tr, np.array(oracle_data["labels"])))
        wave_tr = wave_to_add
        if fluxes_tr.size == 0:
            fluxes_tr = fluxes_oracle
        else:
            fluxes_tr = np.concatenate((fluxes_tr, fluxes_oracle))

    _, indexes = np.unique(filenames_tr, return_index=True)
    indexes = np.sort(indexes)
    filenames_tr = filenames_tr[indexes]
    fluxes_tr = fluxes_tr[indexes]
    labels_tr = labels_tr[indexes]

    if filenames_tr.size == 0:
        raise ValueError("Training data filenames empty")
    if fluxes_tr.size == 0:
        raise ValueError("Training data fluxes empty")
    if labels_tr.size == 0:
        raise ValueError("Training data labels empty")
    if wave_tr.size == 0:
        raise ValueError("Training data wave empty")

    return filenames_tr, wave_tr, fluxes_tr, labels_tr

def get_pool_data(config: ActiveLearningConfig
                  ) -> tuple[NDArray[str], NDArray[float], NDArray[NDArray[float]]]:
    """
    Reads pool data and removes duplicates spectra using filenames.

    Parameters:
        config (ActiveLearningConfig): job's configuration, loaded from configuration file.

    Returns:
        Tuple[NDArray[str], NDArray[float], NDArray[NDArray[float]]:
            1D array of spectrum filenames.
            1D array of spectrum wave.
            2D array of spectrum fluxes.
    """
    filenames, wave, fluxes = file_utils.read_pool_data(config.pool_data_path)
    _, indexes = np.unique(filenames, return_index=True)
    indexes = np.sort(indexes)
    filenames = filenames[indexes]
    fluxes = fluxes[indexes]


    if filenames.size == 0:
        raise ValueError("Pool data filenames empty")
    if fluxes.size == 0:
        raise ValueError("Pool data fluxes empty")
    if wave.size == 0:
        raise ValueError("Pool data wave empty")
    
    return filenames, wave, fluxes

def get_perf_est_list(config: ActiveLearningConfig) -> list[int]:
    """
    Reads performance estimations from previous iteration.

    Parameters:
        config (ActiveLearningConfig): job's configuration, loaded from configuration file.

    Returns:
        If current iteration is 1 empty list, otherwise performance estimations from previous iterations. 
    """
    if config.iteration == 1:
        return []

    with open(config.perf_est_list_path) as f:
        perf_est_list = json.load(f)
    
    if len(perf_est_list) != config.iteration - 1:
        raise ValueError("Perfomance from previous iteration is not provided")
    
    return perf_est_list

def get_indexes(
        config: ActiveLearningConfig, labels_pred: NDArray[int], entropies: NDArray[float]
        ) -> tuple[NDArray[int], NDArray[int], NDArray[int]]:
    """
    Gets spectrum indexes for oracle query, performances 

    Parameters:
        config (ActiveLearningConfig): job's configuration, loaded from configuration file.
        labels_pred (NDArray[int]): 1D array containing labels with the most high probability.
        entropies (NDArray[float]): 1D array containing entropies to each spectrum.

    Returns:
        Tuple[NDArray[int], NDArray[int], NDArray[int]]:
            1D array containing spectrum indexes, which were selected to query oracle.
            1D array containing spectrum indexes, which were selected performance estimation of current job.
            1D array containing spectrum indexes, which were predicted as candidate.
    """
    classes_np = np.array(config.classes)
    candidate_classes_np = np.array(config.candidate_classes)
    mask = np.isin(classes_np, candidate_classes_np)
    classes_indexes = np.where(mask)[0]
    # classes_indexes = np.arange(config.classes.shape[0])[mask]
    mask = np.isin(labels_pred, classes_indexes)
    # candidate_indexes = np.arange(y_labels.shape[0])[mask]
    candidate_indexes = np.where(mask)[0]
    perf_est_batch = min(config.perf_est_batch_size, candidate_indexes.shape[0])
    oracle_indexes = np.argsort(entropies)[-config.oracle_batch_size:]
    perf_est_indexes = np.random.choice(candidate_indexes, size=perf_est_batch, replace=False)
    
    return oracle_indexes, perf_est_indexes, candidate_indexes

def write_prep_data_plot(config: ActiveLearningConfig, result: dict[str, Any]) -> None:
    """
    Writes the data for plot construction on the front-end.

    Parameters:
        config (ActiveLearningConfig): job's configuration, loaded from configuration file.
        result (dict[str, Any]): contains the result of a job, at least has keys:
            filenames (NDArray[str]): 1D array containing spectrum filenames.
            wave (NDArray[float]): 1D array containing spectrum wave from the pool data.
            fluxes (NDArray[NDArray[float]]): 2D array containing spectrum fluxes from the pool data.
            oracle_indexes (NDArray[int]): 1D array containing spectrum indexes, which were selected to query oracle.
            perf_est_indexes (NDArray[int]): 1D array containing spectrum indexes, which were selected perfomance estimation of current job.
            candidate_indexes (NDArray[int]): 1D array containing spectrum indexes, which were predicted as candidate.
    """
    unique_inds = np.unique(np.concatenate((
                result["oracle_indexes"], 
                result["perf_est_indexes"], 
                result["candidate_indexes"] if config.show_candidates else np.array([], dtype=int)
            )))
    
    spectra_fluxes = {}
    filenames, fluxes, wave = result["filenames"], result["fluxes"], result["wave"]
    for i in unique_inds:
        spectra_fluxes[filenames[i]] = fluxes[i].tolist()
    prep_spectra = {
        "wave": wave.tolist(),
        "spectra": spectra_fluxes
    }

    with open(f"{config.result_dir_path}/prep_spectra.json", 'w', encoding='utf-8') as f:
        json.dump(prep_spectra, f, indent=4) 

def write_dim_reduc_data(config: ActiveLearningConfig, fluxes_tr: NDArray[float], 
                         labels_tr: NDArray[int]) -> None:
    """
    Write the data for constructing scatter plot of training data after applying t-SNE on the front-end.

    Parameters:
        config (ActiveLearningConfig): job's configuration, loaded from configuration file.
        fluxes_tr (NDArray[float)): 2D array of fluxes used for model training.
        labels_tr (NDArray[int]): 1D array of labels.
    """
    fluxes_embedded = TSNE(random_state=42).fit_transform(fluxes_tr)
    data = {
        "x": fluxes_embedded[:, 0].tolist(),
        "y": fluxes_embedded[:, 1].tolist(),
        "labels": labels_tr.tolist(),
        "classes": config.classes
    }

    with open(f"{config.result_dir_path}/dim_reduc.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def create_new_config(config: ActiveLearningConfig):
    """
    Creates and saves configuration for next iteration.

    Parameters:
        config (ActiveLearningConfig): job's configuration, loaded from configuration file.
    """
    new_config = config.model_dump(exclude={"result_dir_path", "job_dir"})
    new_config["training_data_path"] = config.job_dir + "/training_data.h5"
    new_config["training_data_to_add_path"] = config.job_dir + "/result.h5"
    new_config["oracle_data_to_add_path"] = config.job_dir + "/oracle_data.json"
    new_config["pool_data_path"] = config.job_dir + "/result.h5"
    new_config["perf_est_list_path"] = config.job_dir + "/perf_est_list.json"
    new_config["iteration"] = config.iteration + 1
    
    with open(f"{config.result_dir_path}/new_config.json", 'w', encoding='utf-8') as f:
        json.dump(new_config, f, indent=4)

def run(config: ActiveLearningConfig):
    """
    Runs regular iteration of active learning job.
    
    1. Loads training and pool data.
    2. Trains model and predicts on it.
    3. Gets corresponding indexes.
    4. Saves results to file and creates severel files.

    Parameters:
        config (ActiveLearningConfig): job's configuration, loaded from configuration file.
    """
    perf_est_list = get_perf_est_list(config)
    filenames_tr, wave_tr, fluxes_tr, labels_tr = get_tr_data(config)
    filenames, wave, fluxes = get_pool_data(config)

    if not np.array_equal(wave_tr, wave):
        raise ValueError("Different waves for pool and training data")

    mask = ~np.isin(filenames, filenames_tr)
    filenames = filenames[mask]
    fluxes = fluxes[mask]

    if filenames.size == 0 or fluxes.size == 0:
        raise ValueError("All data from pool is in training data")
    
    points, num_classes = wave.shape[0], len(config.classes)
    fluxes_tr_bal, labels_tr_bal = cnn_model.balance(fluxes_tr, labels_tr)
    model = cnn_model.get_model(points, num_classes)
    cnn_model.train(model, fluxes_tr_bal, labels_tr_bal, points, num_classes, config)
    label_list_pred = cnn_model.predict(model, fluxes, points, config)
    labels_pred = np.argmax(label_list_pred, axis=1)
    entropies = entropy(label_list_pred.T)

    oracle_indexes, perf_est_indexes, candidate_indexes = get_indexes(config, labels_pred, entropies)

    result = {
        "filenames": filenames,
        "wave": wave,
        "fluxes": fluxes,
        "labels_pred": labels_pred,
        "entropies": entropies,
        "oracle_indexes": oracle_indexes,
        "perf_est_indexes": perf_est_indexes,
        "candidate_indexes": candidate_indexes,
        "model": model,
    }

    write_prep_data_plot(config, result)
    file_utils.write_active_learning_result(f"{config.result_dir_path}/result.h5", config, result)
    file_utils.write_training_data(f"{config.result_dir_path}/training_data.h5", 
                                   filenames_tr, wave_tr, fluxes_tr, labels_tr)
    write_dim_reduc_data(config, fluxes_tr, labels_tr)
    with open(f"{config.result_dir_path}/perf_est_list.json", 'w', encoding='utf-8') as f:
        json.dump(perf_est_list, f, indent=4)
    create_new_config(config)

    return oracle_indexes, perf_est_indexes, candidate_indexes, filenames, labels_pred
