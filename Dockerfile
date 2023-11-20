FROM continuumio/miniconda3 AS condastage

WORKDIR /app

RUN conda install -c conda-forge dlib

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn","app:app","--reload","--host","0.0.0.0" ]

# FROM python:3.9 as pystage

# WORKDIR .

# COPY requirements.txt requirements.txt

# RUN pip3 install --no-cache-dir -r requirements.txt

# CMD [ "uvicorn","app:app","--reload","--host 0.0.0.0"]
