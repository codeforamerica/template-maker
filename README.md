[![Build Status](https://travis-ci.org/codeforamerica/template-maker.svg?branch=master)](https://travis-ci.org/codeforamerica/template-maker)

# template-maker

The template maker is a Flask app that allows you to generate templates and then use those templates to generate documents.

### How is this app organized?

There will be two primary flask blueprints that power this app: **builder** and **consumer**. **Builder** generates templates that can then be turned into actual forms via the **consumer**. The idea is to have a small working set of templates that are used to generate the vast majority of documents, instead of allowing total flexibility every time (a lá something like [formbuilder.js](https://github.com/dobtco/formbuilder) or google forms). The **builder** operates like a single-page application powered by Flask and Postgres to maintain state and angular.js to handle the client-side interaction (see the next section for more detail).

The front-end code is organized into individual component subdirectories in the `static/js/` directory. Front-end tests are stored in the `test` subdirectory of `static`.

### What is this crazy client-side/server-side mixture?

The main guiding philosophy behind the mixture is that [cool URIs don't change](http://www.w3.org/Provider/Style/URI.html). What does that mean for this application in practice? This means that we want to avoid client side routing and rendering as much as possible. Requests should mostly be processed and rendered on the server-side, but where client-side interactivity is necessary, we can use javascript to supplement. Balancing the fact that this is meant to be a web *application* (as opposed to simply a web *site*) means that we try to take advantage of some of the nice client-side interactions that we can gain from using a framework like angular while avoiding some of the problems associated with reliance on a javascript router.

### How do I develop on it?

Good question, thanks for asking! The app is a combination of [Flask](http://flask.pocoo.org/) and [Angular.js](https://angularjs.org/) for the most part. To get it all to run, you'll need to install some dependencies.

##### Developing the Flask Backend

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

##### Developing the Angular frontend

template-maker uses [`npm`](https://github.com/codeforamerica/howto/blob/master/Node.js.md) and [`bower`](http://bower.io/) to manage its front-end dependencies. Ensure you have `npm` and `node` installed (see the howto link for more information), and then run

    $ npm install
    $ bower install

to install the necessary libraries. Because template-maker uses `flask-assets` to actually package and serve assets, you don't need to do anything else, just run the python server as above!

Organizationally, attempt to rely as heavily as possible on directives, and keep controllers as lean as possible. Interpage communications can be handled via the `messageBus` service, but mostly should go through the backend where possible.

### Running Tests

The test suite is split into two parts -- python test and javascript tests.

##### Running the python tests

Python tests are still in the works, and when they are implemented, this document will be updated with additional instructions.

##### Running the javascript tests

The template-maker uses [karma](http://karma-runner.github.io/0.12/index.html) as a test runner and [mocha](http://mochajs.org/) as a testing framework, [chai](http://chaijs.com/) for assertions, and occasionally [sinon](http://sinonjs.org/) for stubbing. The tests run in a [phantom.js](http://phantomjs.org/) headless browser. All test dependencies should have been installed when `npm install` was run above. The tests currently have minimum coverage thresholds to be considered successful; these minimums are defined in the `Gruntfiles`.

Tests are controlled by the `Gruntfile` in the top-level directory. The simplest way to run the tests is to simply run

    $ grunt test:unit

This will run the tests and output a basic coverage report to the console. There are some additional options for running tests as well:

If you want to just run the tests and not deal with coverage reports or any of that, you can use

    $ grunt karma:simple

If you want to continuously be running tests in the background, you can use

    $ grunt karma:continuous

You can also generate more detailed html coverage reports (avalable to view in the coverage-js directory) by running

    $ grunt karma:coverage

### Who made it?

The template maker is a project of the 2015 Pittsburgh Code for America [fellowship team](http://codeforamerica.org/governments/pittsburgh)
