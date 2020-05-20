from utils import RunShellFunc
import os


def download_subject(subject, location):
    download_path=os.path.join(location,f"sub-{subject}")
    if not os.path.exists(os.path.join(location,f"sub-{subject}")):
        os.mkdir(os.path.join(location,f"sub-{subject}"))
    print(f"Downloading Subject {subject} to {download_path}")
    RunShellFunc.run_shell_command(f"aws s3 sync --no-sign-request s3://openneuro.org/ds002152/sub-{subject}/ {location}/sub-{subject}")