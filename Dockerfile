FROM python:3.9-slim
WORKDIR /app
RUN pip install --upgrade pip
COPY reader.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD [ "python3", "-u", "reader.py" ]
