import asyncio
import concurrent.futures
import inspect
from collections import defaultdict
from datetime import date

import numpy as np
import pandas as pd

from j4u_api.database import db_session
from j4u_api.database.models import Feature, FeatureConfig, Group, User

from .qualtrics import qual_client


def min_max_scaler(domain, target, x, inverse=False):
    x = np.clip(x, domain[0], domain[1])
    normalized = (x - domain[0]) / (domain[1] - domain[0])
    res = normalized * (target[1] - target[0]) + target[0]
    if inverse:
        res = target[1] - res + target[0]
    return res


def preprocess_baseline(df, qualtrics_names):
    cols_SC = [(x, df[x].iloc[0]) for x in df.columns if "SC" in x]
    df = df.rename(columns={before: after for before, after in cols_SC})
    df["Sc_Fluency"] = df["COG_VF1"].str.split().apply(
        lambda x: len(x) if type(x) == list else x
    ) + df["COG_VF2"].str.split().apply(lambda x: len(x) if type(x) == list else x)
    df["Sc_Fluency"] *= 0.5
    df = df.loc[
        (df["Finished"] == "1") & df["id"].notnull(),
        ["id"] + [x for x in df.columns if x in qualtrics_names],
    ].dropna()
    df = df.set_index("id")
    df = df.apply(pd.to_numeric)
    df = df.loc[~df.index.duplicated(keep="first")]
    return df


def preprocess_cuiser(df, qualtrics_names):
    df = df.rename(columns={"ID": "id"})
    df = df.loc[
        df["Finished"] == "1", ["id"] + [x for x in df.columns if x in qualtrics_names]
    ].dropna()
    df = df.set_index("id")
    df = df.apply(pd.to_numeric)
    df = df.loc[~df.index.duplicated(keep="first")]
    return df


def thread_dl(id):
    df = qual_client.export_responses(id)
    return df


def scale(df, configs):
    mappers = dict(
        (
            x.qualtrics_name,
            {
                "domain": (x.from_min, x.from_max),
                "target": (x.to_min, x.to_max),
                "inverse": x.inverse,
            },
        )
        for x in configs
    )

    for col, kwargs in mappers.items():
        df[col] = df[col].apply(lambda x: min_max_scaler(**kwargs, x=x))

    return df.round(2)


def get_final_df(surveys_data, configs):
    qualtrics_names = [x.qualtrics_name for x in configs]
    dfs = []
    for group_name, data in surveys_data.items():
        df_baseline = preprocess_baseline(data["baseline"], qualtrics_names)
        df_cruiser = preprocess_cuiser(data["cruiser"], qualtrics_names)
        df = pd.concat([df_baseline, df_cruiser], axis=1, join="inner")
        df["group"] = group_name
        # print(df)
        dfs.append(df)
    df_final = pd.concat(dfs)

    df_final = scale(df_final, configs)

    rename_dict = dict((x.qualtrics_name, x.engine_name) for x in configs)

    df_final = df_final.rename(columns=rename_dict)
    df_final = df_final[
        sorted([x for x in rename_dict.values()], key=lambda x: int(x.split("var")[1]))
    ]

    return df_final


def to_db(df, configs):
    name_to_config_id = {x.engine_name: x.id for x in configs}

    users = User.query.filter(
        User.survey_id.in_(df.index.tolist()), User.form_done == False
    ).all()
    print(f"Updating {len(users)} users ...")
    for user in users:
        features = df.loc[str(user.survey_id)]
        features = list(zip(features.index, features))
        features = [
            Feature(feature_config_id=name_to_config_id[k], user_id=user.id, value=v)
            for k, v in features
        ]
        user.form_done = True
        user.form_done_at = date.today()
        db_session.add(user)
        db_session.bulk_save_objects(features)
        db_session.commit()
    print(f"Done updating.")
    return users


async def gather_dict(d):
    def _gather_objects(container, futures, path):
        if isinstance(container, dict):
            for key, val in container.items():
                _gather_objects(val, path=path + [key], futures=futures)

        if inspect.isawaitable(container):
            futures.append((path, container))

    futures = []
    path = []
    _gather_objects(d, futures, path)
    paths, coros = zip(*futures)
    data = await asyncio.gather(*coros)

    res = {}
    for path, df in zip(paths, data):
        curr_obj = res
        for p in path[:-1]:
            a = curr_obj.get(p, {})
            curr_obj[p] = a
            curr_obj = curr_obj[p]
        curr_obj[path[-1]] = df
    return res


async def main(groups):
    loop = asyncio.get_running_loop()

    futures_dict = {}
    for group in groups:
        dd = {
            "baseline": loop.run_in_executor(None, thread_dl, group.baseline_id),
            "cruiser": loop.run_in_executor(None, thread_dl, group.cruiser_id),
        }
        futures_dict[group.name] = dd

    return await gather_dict(futures_dict)


async def get_features():
    print("Importing Qualtrics data ...")
    groups = Group.query.all()

    configs = FeatureConfig.query.all()

    surveys_data = await main(groups)

    df_final = get_final_df(surveys_data, configs)

    users_updated = to_db(df_final, configs)
    print("Import done.")
    return users_updated
