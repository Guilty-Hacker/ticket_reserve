import uuid

from App.setting import UPLOAD_DIR, FILE_PATH_PREFIX


def filename_transfer(filename):
    exe_name = filename.rsplit(".")[1]
    print(exe_name)
    new_filename = uuid.uuid4().hex + '.' + exe_name
    save_path = UPLOAD_DIR + '/' + new_filename
    upload_path = FILE_PATH_PREFIX + '/' + new_filename
    print(upload_path)
    return save_path,upload_path
