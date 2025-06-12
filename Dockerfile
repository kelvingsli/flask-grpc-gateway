FROM python:3.12 AS builder

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "--app", "app", "run", "-p", "5000", "-h", "0.0.0.0"]
