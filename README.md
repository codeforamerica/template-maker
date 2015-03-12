[![Build Status](https://travis-ci.org/codeforamerica/template-maker.svg?branch=master)](https://travis-ci.org/codeforamerica/template-maker)

# template-maker

## What is it?
The template maker is a Flask app that allows you to generate templates and then use those templates to generate documents.

#### What's the status?
The template-maker is currently a prototype in pre-alpha. We are still both testing the concept and the underlying core UI/UX.

## Who made it?
The template maker is a project of the 2015 Pittsburgh Code for America [fellowship team](http://codeforamerica.org/governments/pittsburgh)

## How
#### Dependencies
The template-maker is a [Flask](http://flask.pocoo.org/) app. It uses [Postgres](http://www.postgresql.org/) for a database and uses [bower](http://bower.io/) to manage most of its dependencies. It also uses [less](http://lesscss.org/) to compile style assets.

It is highly recommended that you use use [virtualenv](https://readthedocs.org/projects/virtualenv/) (and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) for convenience). For a how-to on getting set up, please consult this [howto](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md). Additionally, you'll need node to install bower (see this [howto](https://github.com/codeforamerica/howto/blob/master/Node.js.md) for more on Node), and it is recommended that you use [postgres.app](http://postgresapp.com/) to handle your Postgres (assuming you are developing on OSX).

#### Install
Use the following commands to bootstrap your environment:

**python app**:

    # clone the repo
    git clone https://github.com/codeforamerica/template-maker
    # change into the repo directory
    cd template-maker
    # install python dependencies
    pip install -r requirements.txt

**database**:

    # login to postgres. If you are using postgres.app, you can click
    # the little elephant in your taskbar to open this
    psql
    create database template_maker;

Once you've created your database, you'll need to open `template_maker/settings.py` and edit the DevConfig to use the proper SQLAlchemy database configuration string. Then:

    # upgrade your database to the latest version
    python manage.py db upgrade

**front-end**:

    # install bower
    npm install -g bower
    # use bower to install the dependencies
    bower install

Now, you are ready to roll!

    # run the server
    python manage.py server

#### Testing

Tests are located in the `template_maker_test` directory. To run the tests, run

    PYTHONPATH=. nosetests template_maker_test/

from inside the root directory. For more coverage information, run

    PYTHONPATH=. nosetests template_maker_test/ -v --with-coverage --cover-package=template_maker --cover-erase

## License
See [LICENCE.md](https://github.com/codeforamerica/template-maker/blob/master/LICENCE.md).
