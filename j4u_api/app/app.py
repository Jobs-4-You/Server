from datetime import date

from flask import Flask, render_template, request, send_file
from flask_cors import CORS, cross_origin
from flask_graphql import GraphQLView
from weasyprint import HTML

from config import config
from database import db_session
from gql import schema
from gql.middlewares import auth_middleware

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
        MAIL_PASSWORD=config.EMAIL_PW,
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


@app.route("/certificate", methods=["POST"])
@cross_origin()  # allow all origins all methods.
def certificate():
    content = request.get_json()
    templateData = {
        "civilite": content["civilite"],
        "jobTitle": content["jobTitle"],
        "firstName": content["firstName"],
        "lastName": content["lastName"],
        "birthDate": content["birthDate"],
        "server": "webapp:3000",
        "today": date.today(),
        "timestamp": "timestamp",
    }
    certificate = render_template("certificate.html", **templateData)
    print(certificate)
    HTML(string=certificate).write_pdf("storage/000.pdf")
    return send_file(
        "../storage/000.pdf", as_attachment=True, mimetype="application/pdf"
    )


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
