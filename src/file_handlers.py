import os


class FileHandlers:
    pass

    @staticmethod
    def file_directory(directory: str) -> str:
        """
        Creates a valid directory path regardless of operating system

        Parameters:
        - directory: Name of directory
        """
        return os.path.join(os.getcwd(), directory)

    @staticmethod
    def file_list(directory: str) -> list:
        """
        Creates iterable list of file paths

        Parameters:
        - directory: cwd + directory name
        """
        file_list = {}
        for file in os.listdir(path=directory):
            key = file.lower().split(".")[0]
            value = os.path.join(directory, file)
            file_list[key] = value
        return file_list
