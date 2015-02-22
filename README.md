# template-maker

The template maker is a Flask app that allows you to generate templates and then use those templates to generate documents.

### How is this app organized?

There are two primary flask blueprints that power this app: **builder** and **consumer**. **Builder** generates templates that can then be turned into actual forms via the **consumer**. The idea is to have a small working set of templates that are used to generate the vast majority of documents, instead of allowing total flexibility every time (a lá something like [formbuilder.js](https://github.com/dobtco/formbuilder)). The **builder** operates as a single-page application powered by Flask and Postgres to maintain state, and angular.js to handle the client-side interaction.

### Who made it?

The template maker is a project of the 2015 Pittsburgh Code for America [fellowship team](http://codeforamerica.org/governments/pittsburgh)
