import os.path


def stabilize(test_name: str, file_path: str, expected_extension=".ged"):
    """Get a non-relative path to the file... give test_name as USXX eg US05 and file_path as just the name and .ged extension"""
    INPUT_PATH = "input_files"
    dirpath = os.path.dirname(__file__)
    if not file_path.endswith(expected_extension):
        file_path += expected_extension
    return os.path.join(dirpath, INPUT_PATH, test_name.upper().strip(), file_path)
