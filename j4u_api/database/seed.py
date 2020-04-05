from j4u_api.database import db_session, engine
from j4u_api.database.models import Base, Group, User


def seed_testing():
    print("Start seeding mysql ...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    cog = Group(name="COG")
    cont = Group(name="CONT")
    j4u = Group(name="J4U")
    j4ucog = Group(name="J4UCOG")
    njs = Group(name="NJS")
    j4unjs = Group(name="J4UNJS")

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
        group=j4ucog,
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
        group=cog,
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
        group=cont,
    )

    db_session.add_all([cog, cont, j4u, j4ucog, njs, j4unjs])
    db_session.add_all([admin, other, ather])
    db_session.commit()
    print("Seeding done.")
