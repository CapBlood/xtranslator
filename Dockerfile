FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN apt update
RUN apt install -y libgl1-mesa-glx
RUN apt install -y tesseract-ocr