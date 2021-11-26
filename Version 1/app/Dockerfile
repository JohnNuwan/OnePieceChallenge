

FROM python:3.8-slime

WORKDIR /code

ADD requirements.txt 

RUN pip install -r requirements.txt

COPY app.py 


CMD ["python", "-u", "app.py"]