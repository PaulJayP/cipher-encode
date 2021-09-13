FROM cipher-common

EXPOSE 5001
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /cipher-service
WORKDIR /cipher-service
CMD ["python", "app.py"]
