# Imports
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_graphql import GraphQLView
from data_debts import models
from data_debts.schemas import schema
from flask_graphql_auth import GraphQLAuth
from flask_jwt_extended import JWTManager, create_refresh_token, \
    jwt_refresh_token_required, create_access_token, fresh_jwt_required, \
    jwt_required, JWTManager


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

app.secret_key = 'super=secret'
app.config['JWT_TOKEN_LOCATION'] = 'headers'
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/auth/refresh'
jwt_manager = JWTManager(app)
client = app.test_client()

app.config["JWT_SECRET_KEY"] = "something"  # change this!
jwt = JWTManager(app)
# app.config["REFRESH_EXP_LENGTH"] = 30
# app.config["ACCESS_EXP_LENGTH"] = 10

db = SQLAlchemy(app)


# Routes
@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'admin' or password != 'desafio123':
        return jsonify({"msg": "Bad username or password"}), 401

    ret = {'access_token': create_access_token(username)}
    return jsonify(ret), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({'hello': 'world'}), 200

app.add_url_rule(
    '/graphql',
    view_func=jwt_required(GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True, # for having the GraphiQL interface
        get_context=lambda: {'session': db.session}
    ))
)

def create_app():
    db.init_app(app)
    @app.before_first_request
    def initialize_database():
        """ Create all tables """
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()
    return app

if __name__ == '__main__':
    app.run()