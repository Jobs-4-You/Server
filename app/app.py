# flask_sqlalchemy/app.py
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from database import db_session
from gql import schema
from config import config

app = Flask(__name__)
CORS(app)
app.debug = True


app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True,),
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
