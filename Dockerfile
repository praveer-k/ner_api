FROM python:3.8-slim

WORKDIR /app

COPY ner_api ner_api
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt
  
CMD ["uvicorn", "ner_api.__main__:app", "--host", "0.0.0.0", "--port", "80"]
