import itertools as it
import random
from datetime import datetime

from j4u_api.database import db_session, engine
from j4u_api.database.models import Base, Feature, FeatureConfig, Group, User
from j4u_api.qualtrics import qual_client

baseline_ids = {
    "COG": "SV_emNJjF8ZCQPAyA5",
    "CONT": "SV_9LWr3TrjbpNEdMh",
    "J4U": "SV_eu2KVQoRYyVFsod",
    "J4U+COG": "SV_cVfzu7FqlpU53yl",
    # "NJS": "SV_esuuql0UxehGKfX",
    # "J4U+NJS": "SV_3lAWvHkJlxiWPBz",
}

cruiser_ids = {
    "COG": "SV_af0DlvFQEuZhg8t",
    "CONT": "SV_2fAdbnvAnNMNQgd",
    "J4U": "SV_3PjMqEIEXB52z7T",
    "J4U+COG": "SV_ePrAxjj45PZYMu1",
    # "NJS": "SV_dm75q6TZbF7mEOV",
    # "J4U+NJS": "SV_1ZwZeMCHJD0qrul",
}

features_configs = [
    {
        "qualtrics_name": "Sc_Fluency",
        "engine_name": "var1",
        "from_min": 0,
        "from_max": 30,
        "to_min": 1,
        "to_max": 7,
        "inverse": False,
    },
    {
        "qualtrics_name": "Sc_Tot_IR",
        "engine_name": "var2",
        "from_min": 0,
        "from_max": 8,
        "to_min": 1,
        "to_max": 7,
        "inverse": False,
    },
    {
        "qualtrics_name": "score_matrices",
        "engine_name": "var3",
        "from_min": 0,
        "from_max": 1,
        "to_min": 1,
        "to_max": 7,
        "inverse": False,
    },
    {
        "qualtrics_name": "Sc_WM",
        "engine_name": "var4",
        "from_min": 0,
        "from_max": 12,
        "to_min": 1,
        "to_max": 7,
        "inverse": False,
    },
    {
        "qualtrics_name": "Sc_MOY_RT",
        "engine_name": "var5",
        "from_min": 0,
        "from_max": 5,
        "to_min": 1,
        "to_max": 7,
        "inverse": True,
    },
    {
        "qualtrics_name": "Sc_Verbal_Com",
        "engine_name": "var6",
        "from_min": 0,
        "from_max": 48,
        "to_min": 1,
        "to_max": 7,
        "inverse": False,
    },
    {
        "qualtrics_name": "score_PM",
        "engine_name": "var7",
        "from_min": 0,
        "from_max": 1,
        "to_min": 1,
        "to_max": 7,
        "inverse": False,
    },
    {
        "qualtrics_name": "score_metacog",
        "engine_name": "var8",
        "from_min": 0,
        "from_max": 1,
        "to_min": 1,
        "to_max": 7,
        "inverse": True,
    },
    {
        "qualtrics_name": "Sc_Leader",
        "engine_name": "var9",
        "from_min": 6,
        "from_max": 24,
        "to_min": 1,
        "to_max": 5,
        "inverse": False,
    },
    {
        "qualtrics_name": "Sc_Self_cont",
        "engine_name": "var10",
        "from_min": 13,
        "from_max": 65,
        "to_min": 1,
        "to_max": 5,
        "inverse": False,
    },
    {
        "qualtrics_name": "Sc_Stress_Tol",
        "engine_name": "var11",
        "from_min": 0,
        "from_max": 40,
        "to_min": 1,
        "to_max": 5,
        "inverse": True,
    },
    {
        "qualtrics_name": "Sc_Adapt",
        "engine_name": "var12",
        "from_min": 8,
        "from_max": 40,
        "to_min": 1,
        "to_max": 5,
        "inverse": False,
    },
]


def seed_testing():
    print("Start seeding mysql ...")

    fcs = []
    for x in features_configs:
        fc = FeatureConfig(**x)
        fcs.append(fc)
    db_session.add_all(fcs)
    db_session.flush()

    groups = []
    for (name, baseline_id), (_, cruiser_id) in zip(
        baseline_ids.items(), cruiser_ids.items()
    ):
        g = Group(name=name, baseline_id=baseline_id, cruiser_id=cruiser_id,)
        groups.append(g)

    admin = User(
        civilite="M",
        role="ADMIN",
        first_name="admin",
        last_name="nimda",
        birth_date="2019-01-01",
        phone="0658062948",
        email="admin@example.com",
        password="jdida",
        verified=True,
        group=groups[2],
    )

    group_based_users = []
    group_based_features = []
    for group in groups:
        for i, month in it.product(range(2), range(1, 4)):
            group_mail = "".join([x for x in group.name.lower() if x.isalnum()])
            day = i + 5
            form_done_at = f"2019-{month}-{day}"
            email = f"{group_mail}-{month}-{day}@yopmail.com"
            print(email)

            # qual_client.create_contact(email)

            user = User(
                civilite="M",
                role="USER",
                first_name="John",
                last_name="Doe",
                birth_date="2000-01-01",
                phone=str(random.randint(1e6, 1e7)),
                email=email,
                password="jdida",
                survey_id=str(random.randint(1e8, 1e9)),
                verified=True,
                form_done=True,
                form_done_at=form_done_at,
                group=group,
            )
            db_session.add(user)
            db_session.flush()
            for fc in fcs:
                f = Feature(user_id=user.id, feature_config_id=fc.id, value=3)
                group_based_features.append(f)

    db_session.add(admin)
    db_session.add_all(group_based_users)
    db_session.flush()
    db_session.bulk_save_objects(group_based_features)

    db_session.add_all(groups)
    db_session.commit()
    print("Seeding done.")
