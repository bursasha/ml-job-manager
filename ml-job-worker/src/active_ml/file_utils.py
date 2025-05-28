import h5py
from numpy.typing import NDArray 
from typing import Any

from src.active_ml.config import ActiveLearningConfig

def read_pool_data(file_path: str
                   ) -> tuple[NDArray[str], NDArray[float], NDArray[NDArray[float]]]:
    """
    Reads pool data from HDF5 file.
    HDF5 file must contain following datasets: filenames, wave, fluxes.

    Parameters:
        file_path (str): path to HDF5 file with pool data
    
    Returns:
        Tuple[NDArray[str], NDArray[float], NDArray[NDArray[float]]]:
            1D array of spectra filenames.
            1D array of preprocessed spectra wave.
            2D array with preprocessed fluxes
    """
    with h5py.File(file_path, "r") as h5f:
        filenames = h5f["filenames"].asstr()[:]
        wave = h5f["wave"][:]
        fluxes = h5f["fluxes"][:]
        
    return filenames, wave, fluxes


def read_training_data(file_path: str
                       )-> tuple[NDArray[str], NDArray[float], NDArray[NDArray[float]], NDArray[int]]:
    """
    Reads training data from HDF5 file.
    HDF5 file must contain following datasets: filenames, wave, flux 

    Parameters:
        file_path (str): path to HDF5 file containing training data
    
    Returns:
        Tuple[NDArray[str], NDArray[float], NDArray[NDArray[float]], NDArray[int]]:
            1D array of spectrum filenames.
            1D array of preprocessed spectra wave.
            2D array with preprocessed fluxes.
            1D array of spectrum labels, in integers.
    """
    with h5py.File(file_path, "r") as h5f:
        filenames = h5f["filenames"].asstr()[:]
        wave = h5f["wave"][:]
        labels = h5f["labels"][:]
        fluxes = h5f["fluxes"][:]
    
    return filenames, wave, fluxes, labels

def write_active_learning_result(file_path: str, config: ActiveLearningConfig, 
                                 result: dict[str, Any]) -> None:
    """
    Writes the result of active learning job's regular iteration to HDF5 file.

    Parameters:
        file_path (str): path to HDF5, where result will be written.
        config (ActiveLearningConfig): job's configuration, loaded from configuration file.
        result (dict): contains the result of a job, has keys:
            filenames (NDArray[str]): 1D array containing spectrum filenames.
            wave (NDArray[float]): 1D array containing spectrum wave from the pool data.
            fluxes (NDArray[NDArray[float]]): 2D array containing spectrum fluxes from the pool data.
            labels_pred (NDArray[int]): 1D array containing labels with the most high probability.
            entropies (NDArray[float]): 1D array containing entropies to each spectrum.
            oracle_indexes (NDArray[int]): 1D array containing spectrum indexes, which were selected to query oracle.
            perf_est_indexes (NDArray[int]): 1D array containing spectrum indexes, which were selected perfomance estimation of current job.
            candidate_indexes (NDArray[int]): 1D array containing spectrum indexes, which were predicted as candidate.
            model: model that was trained.
    """
    with h5py.File(file_path, "w") as h5f:
        h5f.create_dataset("filenames", data=result["filenames"].tolist(), dtype=h5py.string_dtype("utf-8"))
        h5f.create_dataset("wave", data=result["wave"])
        h5f.create_dataset("fluxes", data=result["fluxes"])
        h5f.create_dataset("labels", data=result["labels_pred"])
        h5f.create_dataset("entropies", data=result["entropies"])
        h5f.create_dataset("oracle_indexes", data=result["oracle_indexes"])
        h5f.create_dataset("perf_est_indexes", data=result["perf_est_indexes"])

        if config.show_candidates:
            h5f.create_dataset("candidate_indexes", data=result["candidate_indexes"])
        if config.save_model:
            result["model"].save(f"{config.result_dir_path}/model.keras")

def write_active_learning_0_iter(file_path: str, result: dict[str, Any]) -> None:
    """
    Writes the result of active learning job's zero iteration to HDF5 file.

    Parameters:
        file_path (str): path to HDF5, where result will be written.
        result (dict): contains the result of a job, has keys:
            filenames (NDArray[str]): 1D array containing spectrum filenames.
            wave (NDArray[float]): 1D array containing spectrum wave from the pool data.
            fluxes (NDArray[NDArray[float]]): 2D array containing spectrum fluxes from the pool data.
            oracle_indexes (NDArray[int]): 1D array containing spectrum indexes, which were selected to query oracle.
    """
    with h5py.File(file_path, "w") as h5f:
        h5f.create_dataset("filenames", data=result["filenames"].tolist(), dtype=h5py.string_dtype("utf-8"))
        h5f.create_dataset("wave", data=result["wave"])
        h5f.create_dataset("fluxes", data=result["fluxes"])
        h5f.create_dataset("oracle_indexes", data=result["oracle_indexes"])

def write_training_data(file_path: str, filenames: NDArray[str], wave: NDArray[float], 
                        fluxes: NDArray[NDArray[float]], labels: NDArray[int]) -> None:
    """
    Writes the current job's training data 

    Parameters:
        file_path (str): path to HDF5, where training data will be written.
        filenames (NDArray[str]): 1D array containing spectrum filenames.
        wave (NDArray[float]): 1D numpy array containing spectrum wave from the training data.
        fluxes (NDArray[NDArray[float]]): 2D array containing spectrum fluxes from the training data.
        labels (NDArray[int]): 1D array containing labels, in integer.
    """
    with h5py.File(file_path, "w") as h5f:
        h5f.create_dataset("filenames", data=filenames.tolist(), dtype=h5py.string_dtype("utf-8"))
        h5f.create_dataset("wave", data=wave)
        h5f.create_dataset("fluxes", data=fluxes)
        h5f.create_dataset("labels", data=labels)