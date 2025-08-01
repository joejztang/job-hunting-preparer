from utils.envs import RESUMES_PATH, SUGGESTIONS_PATH


def no_resume_exists():
    """
    Check if a resume has been uploaded by the user.
    Returns True if no resume exists, otherwise False.
    """
    for item in RESUMES_PATH.iterdir():
        if item.is_dir() and item.name == "latest":
            return True
    return False
