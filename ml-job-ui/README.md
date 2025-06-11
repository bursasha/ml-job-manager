# ML Job UI

Web interface based on **React**.

# Overview

Web interface for

- Creating, laucning, viewing, deleting the preprocessing and active learning jobs.
- Viewing the platform's storage(file system): uploading and deleting files. Creating and deleting direcotries.
- On the active learning job page:
  - Labeling the spectra.
  - Adding comments to spectra.
  - Viewing plots of preproceessed and raw spectrum.
  - Viewing plot of training data after dimesionality reduction
    (**t-SNE**).
  - Viewing the performance estimation plot.

# Tech Stack

`React`

`Taiwind CSS`

`Vite`

# Running

If web interface need to be run separately, there are two options.

If you have installed npm, run the following commands:

```bash
npm install
npm run dev
```

If you have installed docker and docker compose v2.x:

```bash
docker compose up
```
