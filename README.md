# Information Extraction from EDGAR files

## Overview: 

[notebook slides](https://nbviewer.jupyter.org/format/slides/github/rs-kellogg/edgar2data/blob/main/notebooks/edgar_overview.ipynb)

## Installation with Conda:

```bash
conda create -n edgar python==3.9
conda activate edgar
git clone https://github.com/rs-kellogg/edgar2data.git
cd edgar
pip install .
```

## Running the tests:

```bash
conda install pytest pytest-runner
pytest ./tests
```

## Running the CLI:

```bash
edgar2data --help
```

