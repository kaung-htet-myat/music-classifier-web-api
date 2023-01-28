FROM continuumio/miniconda3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN conda install -c anaconda -y libpq
RUN conda install -c conda-forge -y libsndfile portaudio gcc ffmpeg

WORKDIR /
RUN mkdir -p /app
WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/
