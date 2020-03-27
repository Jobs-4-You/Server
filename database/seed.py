from .models import db_session, engine, Base, User


def seed_testing():
    print("Start seeding mysql ...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    admin = User(
        civilite="M",
        role="ADMIN",
        first_name="admin",
        last_name="nimda",
        birth_date="2019-01-01",
        phone="0658062948",
        email="admin@example.com",
        password="jdida",
        survey_id="12073231",
        verified=True,
        group="J4UCOG",
    )
    other = User(
        civilite="M",
        role="USER",
        first_name="other",
        last_name="nimda",
        birth_date="2019-01-01",
        phone="0658062947",
        email="other@example.com",
        password="jdida",
        verified=True,
        group="COG",
    )
    ather = User(
        civilite="M",
        role="USER",
        first_name="ather",
        last_name="nimda",
        birth_date="2019-01-01",
        phone="0658062949",
        email="ather@example.com",
        password="jdida",
        verified=True,
        group="CONT",
    )

    db_session.add_all([admin, other, ather])
    db_session.commit()
    print("Seeding done.")
