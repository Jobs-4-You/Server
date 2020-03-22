from .models import db_session, engine, Base, User


def seed_testing():
    print("Start seeding mysql ...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    admin = User(
        civilite="M",
        role="ADMIN",
        firstName="admin",
        lastName="nimda",
        birthDate="2019-01-01",
        phone="0658062948",
        email="admin@example.com",
        pwd="jdida",
        surveyId="12073231",
        verified=True,
        group="J4UCOG",
    )
    other = User(
        civilite="M",
        role="USER",
        firstName="other",
        lastName="nimda",
        birthDate="2019-01-01",
        phone="0658062947",
        email="other@example.com",
        pwd="jdida",
        surveyId="12073231",
        verified=True,
        group="COG",
    )
    ather = User(
        civilite="M",
        role="USER",
        firstName="ather",
        lastName="nimda",
        birthDate="2019-01-01",
        phone="0658062949",
        email="ather@example.com",
        pwd="jdida",
        surveyId="12073231",
        verified=True,
        group="CONT",
    )

    db_session.add_all([admin, other, ather])
    db_session.commit()
    print("Seeding done.")
