FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends iputils-ping \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir flask

COPY app.py /app/app.py
COPY flag.txt /flag.txt

EXPOSE 5001

CMD ["python", "app.py"]

