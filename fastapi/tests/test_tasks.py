from fastapi import HTTPException
from fastapi.testclient import TestClient
import requests
from pytest_mock import MockerFixture
from unittest.mock import patch, call
from unittest import TestCase
from worker import uploadFile_task
from main import app
from starlette.testclient import TestClient
import pandas as pd

client = TestClient(app)

def test_getHealthCheck():
    response = client.get("/health")
    assert response.status_code == 200

def getHealthCheck_raiseExept():
    raise requests.exceptions.HTTPError()

def test_getHealthCheck_erro(mocker: MockerFixture):
    mocker.patch("client.test_getHealthCheck", getHealthCheck_raiseExept)
    response = client.get("/health")
    assert response.status_code == 500
    assert response.json() == {"detail": "error occured"}


def test_postTaskPrediction():

    df = pd.DataFrame({
               'state_code': ['CA', 'CA', 'NY', 'NY', 'NY'],
               'municipality_code': ['LA', 'LA', 'NYC', 'NYC', 'BUF'],
               'school_code': ['1', '2', '3', '4', '5'],
               'school_type': ['State', 'Local', 'Federal', 'State', 'State'],
               'school_region': ['Urban', 'Rural', 'Urban', 'Urban', 'Urban'],
               'student_count': [100, 200, 150, 300, 250],
               'internet_availability': ['Yes', 'No', 'Yes', 'NA', 'NA'],
               'internet_availability_prediction': ['Yes', 'No', 'Yes', 'No', 'No'],
           })
    

    dataModeling = {
        "locality_file": df,
        "school_file": df
    }

    response = client.post("/task/prediction",  
                            params=dataModeling,
                            headers={ 'Content-Type': 'application/x-www-form-urlencoded'})
    
    assert response.status_code != 200


def test_getTaskResult():
    task_id = '5984d769-7805-4fdb-81fc-da68fad134fe'
    urlRequest=f"/task/result/{task_id}"
    response = client.get(urlRequest)
    assert response.status_code == 200


def test_getTaskInfo():
    task_id = '5984d769-7805-4fdb-81fc-da68fad134fe'
    urlRequest=f"/task/info/{task_id}"
    response = client.get(urlRequest)
    assert response.status_code != 200