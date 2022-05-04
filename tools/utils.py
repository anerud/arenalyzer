import inspect
import os


def get_relative_file_path(relative_path, stack=1):
    calling_file = inspect.stack()[stack][1]
    return os.path.join(
        os.path.dirname(os.path.abspath(calling_file)),
        relative_path,
    )


def read_relative_file_path(relative_path, mode="r"):
    return open(get_relative_file_path(relative_path, stack=2), mode).read()
