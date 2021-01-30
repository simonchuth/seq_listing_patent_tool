FROM ubuntu:18.04

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=1 \
    PORT=8002 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

RUN apt-get update && apt-get install -y python3.7 python3-pip

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

EXPOSE 8501

COPY src src

CMD streamlit run src/app.py