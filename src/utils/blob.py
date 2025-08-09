import os
import shutil
from datetime import UTC, datetime
from pathlib import Path

from .envs import RESUMES_PATH


def save_to_latest(latest: Path):
    """Move current latest resume to timestamped directory, then save the new latest resume."""
    dashTime = datetime.now(UTC).strftime("%Y-%m-%d-%H-%M-%S")
    if not os.path.exists(RESUMES_PATH / dashTime):
        (RESUMES_PATH / dashTime).mkdir(parents=True)
    if not os.path.exists(RESUMES_PATH / "latest"):
        (RESUMES_PATH / "latest").mkdir(parents=True)

    for item in (RESUMES_PATH / "latest").iterdir():
        if item.is_file():
            shutil.move(str(item.resolve()), str((RESUMES_PATH / dashTime).resolve()))
            break

    shutil.move(str(latest.resolve()), str((RESUMES_PATH / "latest").resolve()))
