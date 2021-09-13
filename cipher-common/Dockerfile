FROM python:3.9.7-slim

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r requirements.txt

COPY . /cipher-common
WORKDIR /cipher-common
RUN python setup.py install
