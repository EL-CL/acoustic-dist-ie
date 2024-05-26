# Code and data for: Acoustic distances of 300 core words imply Indo-European phylogeny and chronology

Code for acoustic distance (AD) calculation between languages, AD-based evolutionary tree generation, dissimilarity metric calculation between trees, and AD-based chronology estimation; as well as data generated from these calculations on 42 Indo-European languages.

<!-- [![DOI](https://zenodo.org/badge/806160451.svg)](https://zenodo.org/badge/latestdoi/806160451) -->

## Audio dataset

The dataset used as the example here, synthesized audio of 300 core words of 42 Indo-European languages, can be retrieved from [Github](https://github.com/EL-CL/acoustic-dist-ie-audio) or [Zenodo](https://zenodo.org/records/11648660). Please place the dataset folder `acoustic-dist-ie-audio` in the parent directory of this repository.

For convenience, it is highly recommended to download the single-file archived dataset from [Github](https://github.com/EL-CL/acoustic-dist-ie-audio/releases/download/v1.0/audios.joblib) or [Zenodo](https://zenodo.org/records/11549487) instead of downloading the original dataset. Please put the archived dataset file `audios.joblib` in the folder of this repository.

You can also create new datasets to conduct AD-based investigations of phylogeny and chronology for other languages.

## Code

Some libraries need to be installed for acoustic feature (AF) extraction, DTW calculation, and clustering:

- [spafe](https://pypi.org/project/spafe/)
- [python_speech_features](https://pypi.org/project/python_speech_features/)
- [dtaidistance](https://pypi.org/project/dtaidistance/)
- [dtw-python](https://pypi.org/project/dtw-python/)
- [biopython](https://pypi.org/project/biopython/)

### Acoustic distance calculation

Run [`acoustic_distance.py`](acoustic_distance.py) to extract AF and compute AD. AF, AF normalization method, DTW method, and AD normalization method can be selected via function parameters. Audio metadata is given in [`audio_metadata.py`](audio_metadata.py). Resulting distance matrices will be saved as `.csv` files in [`acoustic_distances`](acoustic_distances). When run for the first time, the archived audio dataset file `audios.joblib` mentioned above will be generated (if it does not exist) in order to speed up the calculation process.

Since the calculation process is quite time-consuming, please comment out the parameters you do not want to extract in [`acoustic_distance.py`](acoustic_distance.py) (Lines 36–46) to save time. Besides, AD matrices under all parameter combinations are stored in this repository in [`acoustic_distances`](acoustic_distances), so you can quickly skip the AD calculation process and run the following process directly.

<details><summary>Available AFs</summary>

- `BFCC`: Bark-frequency cepstral coefﬁcients
- `CQCC`: Constant Q cepstral coefficients
- `GFCC`: Gammatone frequency cepstral coefficients
- `IMFCC`: Inverse mel-frequency cepstral coefficients
- `LFCC`: Linear frequency cepstral coefficients
- `LPCC`: Linear predictive cepstral coefficients
- `MFCC`: Mel-frequency cepstral coefficients
- `MSRCC`: Magnitude-based spectral root cepstral coefﬁcients
- `NGCC`: Normalized gammachirp cepstral coefficients
- `PNCC`: Power-normalized cepstral coefficients
- `PSRCC`: Phase-based spectral root cepstral coefﬁcients
- `RPLP`: Relative spectra perceptual linear prediction coefficients
- `logFBank`: Logarithmic filter bank energies

</details>

<details><summary>Available AF normalization methods</summary>

- `CMVN`: Cepstral mean and variance normalization
- `CMN`: Cepstral mean normalization
- `MMVN`: Matrix mean and variance normalization
- `MMN`: Matrix mean normalization
- `none`: No normalization

</details>

<details><summary>Available DTW methods</summary>

- `DTW-D`: [Dependent DTW](https://doi.org/10.1007/s10618-016-0455-0)
- `DTW-OE`: [Open-end DTW](https://doi.org/10.1016/j.artmed.2008.11.007)

</details>

<details><summary>Available AD normalization methods</summary>

- `by-sum`: DTW distance divided by the sum of the lengths of two samples
- `by-max`: DTW distance divided by the length of the longer sample
- `none`: No normalization

</details>

### Evolutionary tree generation

Run [`clustering.py`](clustering.py) to generate AD-based evolutionary trees from AD matrices in [`acoustic_distances`](acoustic_distances). Clustering method can be selected via function parameters. Results in Newick format will be saved in [`trees/newicks.tsv`](trees/newicks.tsv).

<details><summary>Available clustering methods</summary>

- `Complete`: Complete-linkage clustering
- `UPGMA`: Unweighted pair group method with arithmetic mean
- `WPGMA`: Weighted pair group method with arithmetic mean
- `UPGMC`: Unweighted pair group method with centroid
- `WPGMC`: Weighted pair group method with centroid
- `Ward`: Ward’s minimum variance method
- `NJ`: Neighbor joining

</details>

### Dissimilarity metric calculation

R packages [Quartet](https://rdocumentation.org/packages/Quartet) and [TreeDist](https://www.rdocumentation.org/packages/TreeDist) need to be installed for dissimilarity metric calculation.

Run [`dissimilarity_metric.r`](dissimilarity_metric.r) in R to compute the Steel–Penny metric and the Robinson–Foulds metric between AD-based trees in [`trees/newicks.tsv`](trees/newicks.tsv) and the reference tree [`trees/reference_tree.nwk`](trees/reference_tree.nwk). Results will be saved as [`trees/dissimilarity_metrics.csv`](trees/dissimilarity_metrics.csv).

The reference tree here is a hierarchy of 42 Indo-European languages sourced from [Glottolog](https://glottolog.org/resource/languoid/id/clas1257) accompanying the dataset.

### Chronology estimation

Run [`fitting.py`](fitting.py) to fit AD and date, and estimate chronology from the AD. Branch and date data of calibration and prediction points are given in `fitting_data.py`. Results will be printed.

## Data

- [`acoustic_distances`](acoustic_distances): AD matrices under all parameter combinations
- [`trees/newicks.tsv`](trees/newicks.tsv): Strings of all AD-based clustering trees in Newick format
- [`trees/reference_tree.nwk`](trees/reference_tree.nwk): The reference tree in Newick format
- [`trees/dissimilarity_metrics.csv`](trees/dissimilarity_metrics.csv): Dissimilarity metrics of all trees
