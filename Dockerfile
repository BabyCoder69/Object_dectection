FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN apt-get update -y && apt-get install -y \
    gcc \
    make \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6

WORKDIR /usr/src/app/
COPY ./ ./

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]