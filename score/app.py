# Imports
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_graphql import GraphQLView
from schemas import schema
from flask_jwt_extended import JWTManager, create_refresh_token, \
    jwt_refresh_token_required, create_access_token, fresh_jwt_required, \
    jwt_required, JWTManager
from models import init_db

basedir = os.path.abspath(os.path.dirname(__file__))

# app initialization
app = Flask(__name__)
app.debug = True
# Configs
app.config['MYSQL_HOST'] = 'mysql_b'
app.config['MYSQL_USER'] = 'my_user'
app.config['MYSQL_PASSWORD'] = 'my_pass'
app.config['MYSQL_DB'] = 'db_b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_HOST'], app.config['MYSQL_DB'])

app.secret_key = 'super=secret'
app.config['JWT_TOKEN_LOCATION'] = 'headers'
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/auth/refresh'
jwt_manager = JWTManager(app)
client = app.test_client()

app.config["JWT_SECRET_KEY"] = "something"
jwt = JWTManager(app)

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


app.add_url_rule(
    '/graphql',
    view_func=jwt_required(GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        get_context=lambda: {'session': db.session}
    ))
)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')