# Official python image version 3.10.11
FROM python:3.10-slim-bullseye 

#Install poetry for dependency management
RUN pip install poetry

#setting the working environment inside the container 
WORKDIR /app 

#Copy contents of the repo to the image 
COPY . /app

#Install dependencies 
RUN poetry install 

RUN chmod +x .venv/bin/activate

WORKDIR /app/python/streamlit 

#Run app 
ENTRYPOINT ["poetry", "run", "streamlit", "run", "0_👋_Introdução.py", "--server.address=0.0.0.0", "--server.port=8501"]