from pathlib import Path


def get_project_root() -> str:
    return Path(__file__).parent.parent.as_posix()

