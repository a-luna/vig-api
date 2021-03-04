FROM tiangolo/uvicorn-gunicorn:python3.8-slim

COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]