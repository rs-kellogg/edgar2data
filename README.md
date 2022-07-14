# Information Extraction from EDGAR files

## Overview: 

[notebook slides](https://nbviewer.jupyter.org/format/slides/github/rs-kellogg/edgar2data/blob/main/notebooks/edgar_overview.ipynb)

## Installation with Conda:

```bash
conda create --name edgar python pip
conda activate edgar

git clone https://github.com/rs-kellogg/edgar2data.git
cd edgar2data
pip install .
```

## Running the tests:

```bash
pip install pytest
pytest ./tests
```

## Running the CLI:

```bash
edgar2data --help
```

## Running the web service:

```bash
uvicorn edgar.api:app
```

## Running the slide deck as a notebook:
```bash
pip install jupyter RISE
jupyter notebook notebooks/edgar_overview.ipynb
```

## Running the slide deck as a voilà app:
```bash
pip install voila
voila --template=reveal notebooks/edgar_overview.ipynb
```


