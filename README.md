# Persistent SQLite for deta.sh

An experimental project to make SQLite database persistent in the
Django project deployed as the [deta.sh](https://deta.sh) micro.

The idea is to load the database file from Deta Drive when Django opens the database connection and then save the database file to Deta Drive when Django closes the connection.

The SQLite database file is placed to the `/tmp` folder when Deta runtime allows writing.

## Caveats

### Concurrency

If multiple instances of your micro are saving the database to Deta Drive,
the last writer will overwrite the file written by the first writer.

The database file will be consistent because Deta Drive API provides
the atomicity of the `put` file operation. However, as mentioned above,
all the changes to the database from the first writer will be lost, because
its database file will be overwritten by the last writer.

It could be okay-ish for your personal project when you know nobody else is using it.

### Time to load and save the database

The load/save cycle is performed literally on every request to Django.

In reality, though, when the database is small, Deta runtime loads and stores
the database file in sub-seconds time. The main visual "slowness" mostly
comes from Django itself.

## Implementation

The module called `persistent_sqlite` is implemented as a runtime patch to `django.db.backends.sqlite3` module of Django.

The patch is developed and tested with Django 4.1.3.

Also, the patch replaces the built-in python module `sqlite3` with `pysqlite3`. Deta runtime provides SQLite 3.7 libraries, but Django 4.1.3 depends on SQLite 3.9.

The patch runs from `wsgi.py` by calling:

    persistent_sqlite.install()

## Dependencies

The dependencies required for Deta are in the `requirements.txt`.

Additionally, you must install local development dependencies to upload and download the database or run the project locally. The local development dependencies are in the `pyproject.toml` file.

    poetry install

## Configuration

A few configuration variables to add to `settings.py`:

`DETA_SQLITE_DB_DRIVE`

This variable sets the Data Drive name (for example, `sqlite.db`). Django
will use this drive to save the database.

The file in this drive will have the name of the database configured in
`DATABASES`.

Before deploying the micro, you need to create the database locally and
upload it to Deta.

    python manage.py migrate
    python manage.py createsuperuser

Before uploading, you must set the `DETA_PROJECT_KEY` variable in your environment.

    python persistent_sqlite.py upload

After this step, you should see the uploaded database file in Deta Drive UI.

Before deploying the micro, you need generate Django static files:

    python manage.py collectstatic

Django runs in non-debug mode to improve performance.

Then you can deploy the micro by:

    deta deploy

If everything is correct, you should be able to see the Django admin panel and log in as a user you created previously.

## Comments

Any further changes in the database schema need to be done locally.

You need to download the database file:

    python persistent_sqlite.py download

This command downloads the database file from Deta to the local directory.

## Running locally

You can run the project locally by:

    python manage.py runserver

or

    gunicorn wsgi:application --reload

Note: when you run the project locally, Django takes the database from the current directory, not from `/tmp`. Also, don't forget to set the `DETA_PROJECT_KEY` variable in your environment.
