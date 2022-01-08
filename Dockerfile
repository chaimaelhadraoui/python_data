FROM python:3.7.9-slim

COPY . /python_data
WORKDIR /python_data
EXPOSE 5000/tcp 8000/tcp
ENV FLASK_APP=/python_data/src/api/app.py 
ENV FLASK_RUN_HOST=0.0.0.0
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN mkdir /root/.streamlit
RUN echo '[general]\nemail = "chaimaehadraoui@gmail.com"' > /root/.streamlit/credentials.toml
RUN chmod +x ./run.sh
CMD sh ./run.sh && flask run
