from flask import render_template
from flask_mail import Message

from j4u_api.app.extensions import mail


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject=subject, sender="j4u@unil.ch", recipients=to)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


def send_mails(tos, subject, template, kwargs_list):
    with mail.connect() as conn:
        for to, kwargs in zip(tos, kwargs_list):
            msg = Message(subject=subject, sender="j4u@unil.ch", recipients=to)
            msg.html = render_template(template + ".html", **kwargs)
            conn.send(msg)
