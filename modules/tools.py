import uuid
import os


def GetUniqueID(static_folder_name, extension):
    filename = str(uuid.uuid4())
    while filename+extension in os.path.join("static", static_folder_name):
        filename = str(uuid.uuid4())
    return filename
