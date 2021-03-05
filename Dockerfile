FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

RUN pip install -U pip setuptools wheel

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

COPY ./app/ /app/app/

ENV DOTENV_FILE=/home/dokku/.env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]