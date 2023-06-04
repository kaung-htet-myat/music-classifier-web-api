FROM continuumio/miniconda3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN conda install -c anaconda -y libpq=12.9
RUN conda install -c conda-forge -y libsndfile=1.2.0 \
                                    portaudio=19.6.0 \
                                    gcc=12.2.0 \
                                    ffmpeg=5.1.2

WORKDIR /
RUN mkdir -p /app
WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/
