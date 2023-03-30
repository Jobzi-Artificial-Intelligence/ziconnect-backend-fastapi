import os
import traceback
import pandas as pd
from pydantic import BaseModel
import pytest

from celery import Celery, states
from celery.exceptions import Reject, Ignore
from celery.utils.log import get_task_logger
from services.internetConnectivityService import (
    SchoolTableProcessor,
    LocalityTableProcessor,
    InternetConnectivityDataLoader,
    InternetConnectivityModel,
    InternetConnectivitySummarizer
)

class TableSchemaError(Exception):
    pass


app = Celery(__name__, include=['worker'])
app.conf.broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
app.conf.update(result_extended=True, task_track_started=True,
                task_store_errors_even_if_ignored=True)
celery_log = get_task_logger(__name__)


@app.task(name="uploadFile_task", acks_late=True)
def uploadFile_task(locality_local_filepath: str, school_local_filepath: str) -> str:
    response = { 'model_metrics': None, 'result_summary': None,
                 'table_schemas': { 'locality': None, 'school': None } }

    try:
        # Load tables
        locality_df = pd.read_csv(locality_local_filepath, sep=',',
                                    encoding='utf-8', dtype=object)
        school_df = pd.read_csv(school_local_filepath, sep=',',
                                 encoding='utf-8', dtype=object)

        # Preprocess tables

        # Process localities table
        locality_processor = LocalityTableProcessor()
        processed_locality = locality_processor.process(locality_df)
        locality_schema_status = { 'is_ok': True, 'failure_cases': None }
        if not processed_locality.is_ok:
            failure_cases = processed_locality.failure_cases.to_dict('records')
            locality_schema_status['is_ok'] = False
            locality_schema_status['failure_cases'] = failure_cases
        response['table_schemas']['locality'] = locality_schema_status

        # Process schools table
        processed_locality_df = processed_locality.final_df

        municipality_codes = None
        if (processed_locality_df is not None
            and 'municipality_code' in processed_locality_df.columns):
            municipality_codes = processed_locality_df['municipality_code']
            municipality_codes = set(municipality_codes.values)

        school_processor = SchoolTableProcessor(municipality_codes)
        processed_school = school_processor.process(school_df)

        school_schema_status = { 'is_ok': True, 'failure_cases': None }
        if not processed_school.is_ok:
            failure_cases = processed_school.failure_cases.to_dict('records')
            school_schema_status['is_ok'] = False
            school_schema_status['failure_cases'] = failure_cases
        response['table_schemas']['school'] = school_schema_status

        # Check whether to reject the task
        if not processed_locality.is_ok or not processed_school.is_ok:
            raise TableSchemaError({
                'exc_type': TableSchemaError.__name__,
                'exc_message': 'Table schema error',
                'schema_error': response
            })

        # Create dataset
        connectivity_dl = InternetConnectivityDataLoader(
            processed_locality.final_df, processed_school.final_df)
        connectivity_dl.setup()

        # Train the model
        model = InternetConnectivityModel()
        model_metrics = model.fit(connectivity_dl.train_dataset)

        # Predict
        full_dataset = pd.concat([connectivity_dl.train_dataset,
                                  connectivity_dl.test_dataset])
        predictions = model.predict(full_dataset)

        # Connectivity summary
        full_dataset['internet_availability_prediction'] = predictions
        summarizer = InternetConnectivitySummarizer()
        result_summary = summarizer.compute_statistics_by_locality(full_dataset)

        response['model_metrics'] = model_metrics
        response['result_summary'] = result_summary
        return response
    except Exception as ex:
        if isinstance(ex, TableSchemaError):
            raise ex
        raise RuntimeError({
            'exc_type': type(ex).__name__,
            'exc_message': ex.args
        })


@app.task(name="uploadSocialImpactFile_task", acks_late=True)
def uploadSocialImpactFile_task(locality_history_local_filepath: str,
                                school_history_local_filepath: str) -> str:
    try:

        # Convert raw tables to dataset
        locality_history_df = pd.read_csv(locality_history_local_filepath, sep=',',
                                          encoding='utf-8', dtype=object)
        school_history_df = pd.read_csv(school_history_local_filepath, sep=',',
                                        encoding='utf-8', dtype=object)

        response = {
            'scenario_distribution': {
                'employability_A': list(range(0, 10)),
                'employability_B': list(range(5, 15)),
            }
        }
        return response

    except Exception as ex:
        raise RuntimeError({
            'exc_type': type(ex).__name__,
            'exc_message': ex.args
        })
