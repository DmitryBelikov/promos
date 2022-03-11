FROM python:3.9

USER root

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./wait-fot-it.sh /code/wait-for-it.sh
RUN chmod +x /code/wait-for-it.sh
COPY ./app /code/app

CMD ["/code/wait-for-it.sh", "postgres:5432", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
