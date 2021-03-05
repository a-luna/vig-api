FROM tiangolo/uvicorn-gunicorn:python3.8

RUN pip install -U pip setuptools wheel

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

COPY ./ /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]