from setuptools import setup, find_packages

setup(
    name="edgar",
    version="0.2.0",
    author="Will Thompson",
    author_email="wkt@northwestern.edu",
    maintainer="Will Thompson",
    maintainer_email="wkt@northwestern.edu",
    description="Code for parsing EDGAR filings",
    url="https://github.com/rs-kellogg/edgar",
    packages=find_packages(include=["edgar", "edgar.*"]),
    package_data={"edgar": ["templates/*.j2"]},
    include_package_data=True,
    install_requires=[
        "dask",
        "pandas",
        "numpy",
        "sqlalchemy",
        "jinjasql",
        "pyyaml",
        "typer[all]",
        "typer-cli",
        "colorama",
        "shellingham",
        "click-spinner",
        "tabulate",
        "tqdm",
        "fastapi",
        "uvicorn[standard]"
    ],
    extras_require={"interactive": ["jupyter", "rise"]},
    entry_points={"console_scripts": ["edgar2data=edgar.cli:app"]},
    setup_requires=["flake8", "black"],
    tests_require=["pytest", "pytest-runner"],
)
