# 🛠️ ML Job Worker

**Celery‐based Worker** for executing ML jobs (Data Preprocessing & Active ML). 

Built with `Celery`, `TensorFlow`, `Scikit-Learn`, `Astropy` and `HTTPX`.

---

## 🔍 Overview

The **ML Job Worker** runs two types of background jobs, triggered by the **ML Job API**:


1. **Data Preprocessing**  

   – Reads FITS spectra, interpolates flux onto a uniform grid, scales & writes an `HDF5`.  
   
   – Reports completion/failure back to the API.


2. **Active ML**  
   
   – Iteratively trains a 1D-CNN on preprocessed data, selects oracle/performance/candidate sets.  
   
   – Writes `HDF5` and `JSON` outputs for each iteration.  
   
   – Initializes batch “labelling” records via the **ML Job API** and signals job end.


All shared files (raw spectra, configs, results, logs) live on a host-mounted filesystem.  

---

## 📍 Features

- `Celery 5.5` Worker receives jobs from `AMQP` `RabbitMQ` broker - **ML Job Queue.**  

- `Pydantic` settings + DTOs for config validation.  

- `TensorFlow 2.16` + `Keras` CNN for spectrum classification.  

- `Scikit-Learn` (SMOTE, t-SNE), `SciPy`, `NumPy`, `Astropy`.  

- `HTTPX` client to notify **ML Job API** of job progress and initialize labellings.  

- Robust error handling and automatic retry on broker connectivity.

---

## ⚙️ Tech Stack

- `Python 3.11`  

- `Celery 5.5`

- `Pydantic`

- `TensorFlow 2.16` (CUDA-enabled)  

- `Scikit-Learn 1.6`, `SciPy 1.15`, `NumPy 1.26`

- `HTTPX` for HTTP callbacks  

- `Astropy` for FITS parsing

- **HDF5** via `h5py`  

- `Docker` & `Docker Compose`
