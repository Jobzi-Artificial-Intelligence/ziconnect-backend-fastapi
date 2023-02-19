import json

from unittest.mock import patch, call

from worker import create_task

def test_task():
    assert create_task.run(1)
    assert create_task.run(2)
    assert create_task.run(3)

@patch("worker.create_task.run")
def test_mock_task(mock_run):
    assert create_task.run(1)
    create_task.run.assert_called_once_with(1)

    assert create_task.run(2)
    assert create_task.run.call_count == 2

    assert create_task.run(3)
    assert create_task.run.call_count == 3


