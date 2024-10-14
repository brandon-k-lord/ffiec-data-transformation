import os


class FileHandlers:
    pass

    @staticmethod
    def file_directory(directory: str) -> str:
        return os.path.join(os.getcwd(), directory)

    @staticmethod
    def file_list(directory: str) -> list:
        file_list = {}
        for file in os.listdir(path=directory):
            key = file.lower().split(".")[0]
            value = os.path.join(directory, file)
            file_list[key] = value
        return file_list

    @staticmethod
    def script_list(directory: str) -> list:
        file_list = {}
        for file in os.listdir(path=directory):
            key = file.lower().split(".")[0]
            value = os.path.join(directory, file)
            file_list[key] = value
        return file_list
