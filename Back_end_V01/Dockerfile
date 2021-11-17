
# Chargement image python
FROM python:3.8-slim

# Dossier 
WORKDIR /code

#Docker which additional commands to execute.
ADD requirements.txt 

RUN pip install requirements.txt

COPY main.py 


CMD ["python", "-u", "main.py"]