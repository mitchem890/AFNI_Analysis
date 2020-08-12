import sys
sys.path.append("..") # Adds higher directory to python modules path.
from classes import Images
from classes import TaskGLMs
from utils import Validate_User_Input
import pytest


@pytest.mark.parametrize("pipeline",[("hcp"),("fmriprep")])
def test_validate_pipeline(pipeline):
    assert Validate_User_Input.validate_pipeline(pipeline) is True


def test_validate_pipeline_error():
    with pytest.raises(OSError):
        Validate_User_Input.validate_pipeline("badInput")


@pytest.mark.parametrize("subjects",[(["132017"]),(["DMCC012345"])])
def test_validate_subjects(subjects):
    assert Validate_User_Input.validate_subjects(subjects)


def test_validate_subjects_error():
    with pytest.raises(OSError):
        Validate_User_Input.validate_subjects("badInput")


@pytest.mark.parametrize("wave", [("wave1"), ("wave2")])
def test_validate_wave(wave):
    assert Validate_User_Input.validate_wave(wave)


def test_validate_wave_error():
    with pytest.raises(OSError):
        Validate_User_Input.validate_wave("badInput")


@pytest.mark.parametrize("tasks", [(["Axcpt", "Cuedts", "Stern", "Stroop"])])
def test_validate_tasks(tasks):
    assert Validate_User_Input.validate_tasks(tasks)


def test_validate_tasks_error():
    with pytest.raises(OSError):
        Validate_User_Input.validate_tasks("badInput")


@pytest.mark.parametrize("sessions", [(["baeline", "proactive", "reactive"])])
def validate_sessions(sessions):
    assert Validate_User_Input.validate_sessions(sessions)


def test_validate_sessions_error():
    with pytest.raises(OSError):
        Validate_User_Input.validate_sessions("badInput")


@pytest.mark.parametrize("ncpus", [("1"), ("3"), ("10")])
def tests_validate_ncpus(ncpus):
    assert Validate_User_Input.validate_ncpus(ncpus)


def test_validate_ncpus_error():
    with pytest.raises(ValueError):
        Validate_User_Input.validate_ncpus("badInput")
