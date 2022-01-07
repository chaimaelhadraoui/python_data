## Solution Dockerized
Requirements:
 - docker engine
 - docker compose

if you have docker-compose/docker engine in your envirement you can use it instead of pipenv, just by running the command:
```sh
      docker-compose up 
```
Or if you like to detache the container you can use `-d` option.

Please make sure you are not running any application that use the port `5000` and `8000`. 
If you encountered permission issue just run `chmod +x ./run.sh`

If you like to run pytest for unit testing, please make sure the container is running and  use this command:
```sh
     docker exec -it python_data pytest
```

Otherwise, If you want to use pipenv, please don't forget to install requirements using Pipefile.lock or requirements.txt by running `pip install -r requirements.txt`

# Python Data 

## Requirements
- Python 3.7 or higher.
#### - Install pipenv on your global python setup
```Python
    pip install pipenv 
```
Or follow [documentation](https://pipenv.pypa.io/en/latest/install/) to install it properly on your system
#### - Install requirements
```sh
    cd python-data-assignement
```
```Python
    pipenv install
```
```Python
    pipenv shell
```
#### - Start the application
```sh
    sh run.sh
```
- API : http://localhost:5000
- Streamlit Dashboard : http://localhost:8000

P.S You can check the log files for any improbable issues with your execution.

## Description
This mini project is a data app that revolves around credit card fraud detection.

You are given a `dataset` that contains a number of transactions.

Each row of the dataset contains:
- Features that were extracted using dimensionality reduction with `PCA` 
- The transaction amount
- A flag `[0,1]` that tells you whether a transaction is clear or fraudulent.

The project contains by default:
- A baseline `decision tree model` trained on the aforementioned dataset
- An `API` that exposes an `inference endpoint` for predictions using the baseline model
- A streamlit dashboard divided on three parts `(Exploratory Data Analysis, Training, Inference)`
