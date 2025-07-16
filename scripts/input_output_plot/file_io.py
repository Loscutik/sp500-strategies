from typing import Any

def fetch_file(url: str, folder: str, filename: str | None = None) -> str:
    """
    get a file from the given url  and save it to the 'folder' with the given filename.
    Creates the folder if it doesn't exist
    """
    import requests
    import os
    if filename is None:
        filename = url.split('/')[-1]
    path_destination = os.path.join(folder, filename)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(path_destination):
        response = requests.get(url,stream=True)
        with open(path_destination, 'wb') as file_destination:
            for chunk in response.iter_content(chunk_size=128):
                file_destination.write(chunk)

    return path_destination


def csv_filepath_to_dataframe(filepath: str) -> None:
    """
    reads a .csv file with a comma as the separator and returns a dataframe
    """
    import pandas
    return pandas.read_csv(
        filepath,
        sep=',',
        engine='pyarrow',
    )

def save_data_as_txt(data: Any, folder: str, filename: str) -> None:
    """
    save the data to a <folder>/<filename> file in text mode
    """
    import os
    if not os.path.exists(folder):
        os.makedirs(folder)
    path_destination = folder+filename

    if isinstance(data, str):
        data_as_string = data 
    else:
        data_as_string = data.to_string()

    with open(path_destination, 'w') as outfile:
        outfile.write(data_as_string)


def unzip_file(path_zip: str, dir_destination: str) -> None:
    """
    extract files from `path_zip` to destination `dir_destination` directory
    """
    import zipfile

    with zipfile.ZipFile(path_zip, 'r') as zip_ref:
        zip_ref.extractall(dir_destination)
