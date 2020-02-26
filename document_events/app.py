# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_graphql import GraphQLView
from document_events.schemas import schema



basedir = os.path.abspath(os.path.dirname(__file__))

# app initialization
app = Flask(__name__)
app.debug = True
# Configs
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '$hAdOw8rUn5'
app.config['MYSQL_DB'] = 'db_a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_HOST'], app.config['MYSQL_DB'])


client = app.test_client()

db = SQLAlchemy(app)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        get_context=lambda: {'session': db.session}
    )
)


if __name__ == '__main__':
    app.run()