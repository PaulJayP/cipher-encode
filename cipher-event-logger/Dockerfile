FROM cipher-common

EXPOSE 5002
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /cipher-event-logger
WORKDIR /cipher-event-logger
CMD ["python", "app.py"]
