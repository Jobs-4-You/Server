import glob
import os
import uuid
from datetime import date

from flask import Flask, render_template, request, send_file
from flask_cors import CORS, cross_origin
from flask_graphql import GraphQLView
from weasyprint import HTML

import j4u_api.elastic_db
from j4u_api.config import config
from j4u_api.database import db_session
from j4u_api.gql import schema
from j4u_api.gql.middlewares import auth_middleware
from j4u_api.utils.logging import logger

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
    try:
        content = request.get_json()
        templateData = {
            "civilite": content["civilite"],
            "jobTitle": content["jobTitle"],
            "firstName": content["firstName"],
            "lastName": content["lastName"],
            "birthDate": content["birthDate"],
            "server": config.APP_DOCKER_URL,
            "today": date.today(),
            "timestamp": "timestamp",
        }
        certificate = render_template("certificate.html", **templateData)
        uuid_name = f"{str(uuid.uuid4())}.pdf"
        pdf_temp_path = os.path.join(config.CERT_TEMP_PATH, uuid_name)
        HTML(string=certificate).write_pdf(pdf_temp_path)
        return send_file(pdf_temp_path, as_attachment=True, mimetype="application/pdf")
    except Exception as err:
        print(err)
        print(err)
        print(err)
        print(err)
        print(err)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    trash_pdfs = glob.glob(f"{config.CERT_TEMP_PATH}/*.pdf")
    for pdf in trash_pdfs:
        os.remove(pdf)
    n_removed = len(trash_pdfs)
    logger.info(
        __name__,
        shutdown_session,
        "%d temp certificate PDFs removed",
        n_removed,
        extra={"cert_temp_pdfs_removed": n_removed},
    )
