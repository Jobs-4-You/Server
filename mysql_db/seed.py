from .models import mysql_session, engine, Base, User


def seed_testing():
    print("Start seeding mysql ...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    admin = User(
        civilite="M",
        firstName="admin",
        lastName="nimda",
        birthDate="2019-01-01",
        phone="0658062948",
        email="admin@example.com",
        pwd="jdida",
        plastaId="a111111",
        surveyId="12073231",
        verified=True,
        blocked=False,
        fixedOldJobValue=False,
        fixedAlphaBeta=False,
        group="J4U+COGG",
    )
    other = User(
        civilite="M",
        firstName="other",
        lastName="nimda",
        birthDate="2019-01-01",
        phone="0658062947",
        email="other@example.com",
        pwd="jdida",
        plastaId="009",
        # surveyId="17813205",
        surveyId="12073231",
        verified=True,
        blocked=False,
        group="COG",
    )
    ather = User(
        civilite="M",
        firstName="ather",
        lastName="nimda",
        birthDate="2019-01-01",
        phone="0658062949",
        email="ather@example.com",
        pwd="jdida",
        plastaId="003",
        # surveyId="86930465",
        surveyId="12073231",
        verified=True,
        group="CONT",
    )

    mysql_session.add_all([admin, other, ather])
    mysql_session.commit()
    print("Seeding done.")
