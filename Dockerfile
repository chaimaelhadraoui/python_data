FROM python:3.7.9-slim

COPY . /python_data
WORKDIR /python_data
EXPOSE 5000/tcp 8000/tcp
ENV FLASK_APP=/python_data/src/api/app.py 
ENV FLASK_RUN_HOST=0.0.0.0
RUN apt-get update && apt-get install curl -y
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN mkdir /root/.streamlit
RUN curl --create-dirs -O --output-dir /python_data/input https://gitlab.com/chaimaelhadraoui/python_data_assignment/-/blob/master/input/creditcard.csv
RUN echo '[general]\nemail = "chaimaehadraoui@gmail.com"' > /root/.streamlit/credentials.toml
RUN chmod +x ./run.sh
CMD sh ./run.sh && flask run
