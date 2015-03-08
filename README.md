[![Build Status](https://travis-ci.org/codeforamerica/template-maker.svg?branch=master)](https://travis-ci.org/codeforamerica/template-maker)

# template-maker

The template maker is a Flask app that allows you to generate templates and then use those templates to generate documents.

### How is this app organized?

### How do I develop on it?

It is highly recommended that you use use [virtualenv](https://readthedocs.org/projects/virtualenv/) (and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) for convenience). For a how-to on getting set up, please consult this [howto](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md). Note that these steps assume you have a postgres database named `template_maker` running locally.

Then run the following commands to bootstrap your environment:

    # clone the repo
    git clone https://github.com/codeforamerica/template-maker
    # change into the repo directory
    cd template-maker
    # install python dependencies
    pip install -r requirements.txt
    # upgrade your database to the latest version
    python manage.py db upgrade
    # run the server
    python manage.py server

NOTE: If this is the first time that you are working with template-maker, be sure to run the following command (before starting your server) to stamp your database and allow for future migrations:

    python manage.py db stamp head

If installing requirements from pip breaks on `psycopg2`, make sure that your `$PATH` includes your Postgres installation's `bin/` directory. For example, if you installed [postgres.app](http://postgresapp.com/), try this:

    export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin/
    pip install -r requirements.txt

### Running Tests

Python tests are still in the works, and when they are implemented, this document will be updated with additional instructions.

### Who made it?

The template maker is a project of the 2015 Pittsburgh Code for America [fellowship team](http://codeforamerica.org/governments/pittsburgh)
