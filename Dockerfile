from python:3.9-slim
WORKDIR /app
RUN pip install --upgrade pip
COPY --chown=reader:reader reader.py .
COPY --chown=reader:reader requirements.txt .
RUN pip install -r requirements.txt
CMD [ "python3", "-u", "reader.py" ]
