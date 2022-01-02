FROM python:3.8-slim-buster

WORKDIR /flask_app

COPY requirements.txt requirements.txt

RUN apt-get -y update && apt-get install -y build-essential && pip3 install -r requirements.txt && apt-get install ffmpeg libsm6 libxext6  -y

COPY math_symbols.h5 math_symbols.h5
COPY static/ static/
COPY imgs/ imgs/
COPY templates/ templates/
COPY *.py ./

CMD ["python3", "flask_app.py"]