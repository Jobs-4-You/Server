from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from database import db_session
from gql import schema
from gql.middlewares import auth_middleware
from config import config
from .extensions import mail

app = Flask(__name__, template_folder="../storage/templates/")
CORS(app)
app.debug = True

app.config.update(
    dict(
        MAIL_SUPPRESS_SEND=False,
        TESTING=False,
        MAIL_DEBUG=False,
        MAIL_USE_TLS=True,
        MAIL_SERVER="smtp.unil.ch",
        MAIL_PORT=587,
        MAIL_USERNAME=config.EMAIL_USER,
        MAIL_PASSWORD=config.EMAIL_PWD,
    )
)

mail.init_app(app)
# with mail.connect() as conn:
#    print(conn)


app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql", schema=schema, graphiql=True, middleware=[auth_middleware]
    ),
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
