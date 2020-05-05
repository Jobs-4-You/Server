import time

from j4u_api.app.app import app
from j4u_api.config import config
from j4u_api.qualtrics.get_features import get_features
from j4u_api.utils.mail import send_mails


def get_features_and_send_emails():
    users = get_features()
    with app.app_context():
        if users is not None and len(users) > 0:
            tos = [[user.email] for user in users]
            print(tos)
            kwargs_list = [{"link": f"{config.APP_URL}/?login"}] * len(users)
            send_mails(
                tos=tos,
                subject="Données importées avec succès",
                template="export-done",
                kwargs_list=kwargs_list,
            )
    return len(users)


while True:
    try:
        n_updated = get_features()
        print(f"{n_updated} users updated")
    except Exception as err:
        print(err)
    time.sleep(15)
