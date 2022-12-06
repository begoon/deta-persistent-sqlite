import os
import sys
from pathlib import Path

import settings
from deta import Deta
from django.utils.asyncio import async_unsafe

drive = Deta().Drive(settings.DETA_SQLITE_DB_DRIVE)

remote_name = settings.DETA_SQLITE_DB_FILE
local_name = settings.DETA_SQLITE_DB_LOCAL_FILE

original_get_new_connection = None
original_close = None


def download_database() -> None:
    stream = drive.get(remote_name)
    assert stream
    with open(local_name, "wb+") as f:
        for chunk in stream.iter_chunks(4096):
            f.write(chunk)
        stream.close()


def upload_database() -> None:
    with open(local_name, 'rb') as f:
        drive.put(remote_name, f)


@async_unsafe
def patched_get_new_connection(self, conn_params):
    download_database()
    conn_params["database"] = local_name
    return original_get_new_connection(self, conn_params)


@async_unsafe
def patched_close(self):
    result = original_close(self)
    upload_database()
    return result


def patch_sqlite_database_wrapper():
    from django.db.backends.sqlite3 import base

    global original_get_new_connection, original_close

    original_get_new_connection = base.DatabaseWrapper.get_new_connection
    base.DatabaseWrapper.get_new_connection = patched_get_new_connection

    original_close = base.DatabaseWrapper.close
    base.DatabaseWrapper.close = patched_close


def install_pysqlite3() -> None:
    global original_get_new_connection, original_close

    if os.getenv('DETA_RUNTIME'):
        __import__('pysqlite3')

        sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


def install() -> None:
    install_pysqlite3()
    patch_sqlite_database_wrapper()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python3 persistent_sqlite.py upload | download [-f]")
        sys.exit(1)

    if sys.argv[1] == 'upload':
        upload_database()

    if sys.argv[1] == 'download':
        force = len(sys.argv) > 2 and sys.argv[2] == '-f'
        if Path(local_name).exists() and not force:
            print(local_name, "already exists")
            sys.exit(1)
        download_database()
