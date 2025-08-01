import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
if os.getenv("JOB_HUNTING_CONTENTS") is None:
    raise ValueError(
        "please set a path to the JOB_HUNTING_CONTENTS environment variable"
    )

RESUMES_PATH = Path(os.getenv("JOB_HUNTING_CONTENTS")) / "resumes"
SUGGESTIONS_PATH = Path(os.getenv("JOB_HUNTING_CONTENTS")) / "suggestions"
