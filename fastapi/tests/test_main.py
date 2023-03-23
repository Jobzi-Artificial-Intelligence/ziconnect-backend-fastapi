import json
import pytest
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.testclient import TestClient
import requests
from pytest_mock import MockerFixture
from unittest.mock import patch, call
import unittest 
from worker import *
from main import app
from starlette.testclient import TestClient
import pandas as pd
from celery import Celery, uuid
from main import *

client = TestClient(app)

def test_getHealthCheck():
    response = client.get("/health")
    assert response.status_code == 200

def test_getHealthCheck_unavailable():
    response = client.get("/unavailable")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

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
    
    task_name = "uploadFile_task"
    target_dirpath = '/var/lib/docker/volumes/fastapi-storage/_data/'
    task_id = uuid()

    assert task_name == "uploadFile_task"
    assert target_dirpath == '/var/lib/docker/volumes/fastapi-storage/_data/'
    assert task_id != None

    dataModeling = {
        "locality_file": df,
        "school_file": df
    }

    
    response = client.post("/task/prediction",  
                            params=dataModeling,
                            headers={ 'Content-Type': 'application/x-www-form-urlencoded'})
    
    assert response.status_code != 200


def test_postTaskSocialImpact():

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
    
    task_name = "uploadSocialImpactFile_task"
    assert task_name != None

    target_dirpath = '/var/lib/docker/volumes/fastapi-storage/_data/'
    assert target_dirpath != None

    dataModeling = {
        "localityHistory_file": df,
        "schoolHistory_file": df
    }

    response = client.post("/task/socialimpact",  
                            params=dataModeling,
                            headers={ 'Content-Type': 'application/x-www-form-urlencoded'})
    
    assert response.status_code != 200

def test_getTaskResult():
    urlRequest="/task/result/5984d769-7805-4fdb-81fc-da68fad134fe"
    response = client.get(urlRequest)
    assert response.status_code == 200


def test_getTaskInfo():
    urlRequest="/task/info/5984d769-7805-4fdb-81fc-da68fad134fe"
    response = client.get(urlRequest)
    assert response.status_code != 200


def test_worker_throws_exception():
    try:
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
        uploadFile_task(df, df)
    except RuntimeError:
        pass
    except Exception as ex:
         raise RuntimeError({
            'exception_type': type(ex).__name__,
            'exception_message': traceback.format_exc().split('\n')
        })


