FROM gcc:12 AS build

WORKDIR /app

ADD ht2000.c /app/ht2000.c

RUN gcc -o ht2000 ht2000.c

FROM python:3.12-slim

WORKDIR /app

COPY --from=build /app/ht2000 /app/ht2000

ADD homeassistant/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD homeassistant/ha.py /app/ha.py

CMD ["python", "/app/ha.py"]
