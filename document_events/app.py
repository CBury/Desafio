# Imports
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_graphql import GraphQLView
from schemas import schema
from models import init_db

basedir = os.path.abspath(os.path.dirname(__file__))

# app initialization
app = Flask(__name__)
app.debug = True
# Configs
app.config['MYSQL_HOST'] = 'mysql_c'
app.config['MYSQL_USER'] = 'my_user'
app.config['MYSQL_PASSWORD'] = 'my_pass'
app.config['MYSQL_DB'] = 'db_c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_HOST'], app.config['MYSQL_DB'])


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
    init_db()
    app.run(host='0.0.0.0')