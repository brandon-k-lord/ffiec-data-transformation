import os
from typing import List


class FileHandler:
    @staticmethod
    def create_file_dict(directory: str) -> dict[str, str]:
        """
        Creates iterable dict of file paths.

        Key: filename
        value: absolute file path

        Parameters:
        - directory: directory name
        """
        wk_dir = os.path.join(os.getcwd(), directory)
        return {
            file.lower().split(".")[0]: os.path.join(wk_dir, file)
            for file in os.listdir(path=wk_dir)
        }
