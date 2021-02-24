from setuptools import setup, find_packages

setup(
    name="edgar2data",
    version="0.2.0",
    author="Will Thompson",
    author_email="wkt@northwestern.edu",
    maintainer="Will Thompson",
    maintainer_email="wkt@northwestern.edu",
    description="Code for parsing EDGAR filings",
    url="https://github.com/rs-kellogg/edgar2data",
    packages=find_packages(include=["edgar", "edgar.*"]),
    package_data={"edgar": ["templates/*.j2"]},
    include_package_data=True,
    install_requires=[
        "dask==2021.2.0 ",
        "pandas==1.2.2",
        "pyyaml==5.4.1",
        "typer[all]==0.3.2",
        "typer-cli==0.0.11",
        "colorama==0.4.4",
        "shellingham==1.4.0",
        "click-spinner==0.1.10",
        "tabulate==0.8.7",
        "tqdm==4.56.2",
        "fastapi==0.63.0",
        "uvicorn==0.13.3",
        "spacy==3.0.3"
    ],
    extras_require={"interactive": ["jupyter", "rise"]},
    entry_points={"console_scripts": ["edgar2data=edgar.cli:app"]},
    setup_requires=["black"],
    tests_require=["pytest"],
)
