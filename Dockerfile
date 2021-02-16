FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN pip install --upgrade pip

WORKDIR /app

COPY ./edgar /app/edgar
COPY ./setup.py /app
COPY ./edgar/api.py /app/main.py

RUN pip install .
RUN python -m spacy download en_core_web_md



