from flask_mail import Message
from flask import render_template
from app.extensions import mail


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject=subject, sender="j4u@unil.ch", recipients=to)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
