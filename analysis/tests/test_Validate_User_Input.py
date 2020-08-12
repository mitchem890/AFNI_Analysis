import sys
sys.path.append("..") # Adds higher directory to python modules path.
from classes import Images
from classes import TaskGLMs
from utils import Validate_User_Input
import pytest


@pytest.mark.parametrize("pipeline",[("hcp"),("fmriprep")])
def test_validate_pipeline(pipeline):

    assert Validate_User_Input.validate_pipeline(pipeline) is None

def test_validate_pipeline_error():
    with pytest.raises(IOError):
        assert Validate_User_Input.validate_pipeline("badInput")