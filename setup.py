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
        "typer[all]==0.6.1",
        "lxml==4.9.1",
        "pandas==1.4.3",
        "pyyaml==6.0",
        "fastapi==0.78.0",
        "uvicorn==0.18.2",
        "requests==2.28.1"
    ],
    entry_points={"console_scripts": ["edgar2data=edgar.cli:app"]},
    extras_require={"interactive": ["jupyter", "rise"]},
    tests_require=["pytest"],
)
