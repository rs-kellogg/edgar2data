# Information Extraction from EDGAR files

## Overview: 

[notebook slides](https://nbviewer.jupyter.org/format/slides/github/rs-kellogg/edgar2data/blob/main/notebooks/edgar_overview.ipynb)

## Installation with Conda:

```bash
conda create -n edgar python
conda activate edgar
git clone https://github.com/rs-kellogg/edgar2data.git
cd edgar
pip install .
python -m spacy download en_core_web_md
```

## Running the tests:

```bash
conda install pytest
pytest ./tests
```

## Running the CLI:

```bash
edgar2data --help
```

## Running the slide deck as a notebook:
```bash
jupyter notebook notebooks/resilient-code.ipynb
```

## Running the slide deck as a voilà app:
```bash
voila --template=reveal notebooks/resilient-code.ipynb
```

