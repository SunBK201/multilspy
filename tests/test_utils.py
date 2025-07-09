import contextlib
import os
import pathlib
import shutil
from typing import Iterator
from uuid import uuid4

from scubalspy.scubalspy_config import ScubalspyConfig
from scubalspy.scubalspy_logger import ScubalspyLogger
from scubalspy.scubalspy_utils import FileUtils
from tests.scubalspy.multilspy_context import ScubalspyContext


@contextlib.contextmanager
def create_test_context(params: dict) -> Iterator[ScubalspyContext]:
    """
    Creates a test context for the given parameters.
    """
    config = ScubalspyConfig.from_dict(params)
    logger = ScubalspyLogger()

    user_home_dir = os.path.expanduser("~")
    scubalspy_home_directory = str(pathlib.Path(user_home_dir, ".scubalspy"))
    temp_extract_directory = str(pathlib.Path(scubalspy_home_directory, uuid4().hex))
    try:
        os.makedirs(temp_extract_directory, exist_ok=False)
        assert params['repo_url'].endswith('/')
        repo_zip_url = params['repo_url'] + f"archive/{params['repo_commit']}.zip"
        FileUtils.download_and_extract_archive(logger, repo_zip_url, temp_extract_directory, "zip")
        dir_contents = os.listdir(temp_extract_directory)
        assert len(dir_contents) == 1
        source_directory_path = str(pathlib.Path(temp_extract_directory, dir_contents[0]))

        yield ScubalspyContext(config, logger, source_directory_path)
    finally:
        if os.path.exists(temp_extract_directory):
            shutil.rmtree(temp_extract_directory)
