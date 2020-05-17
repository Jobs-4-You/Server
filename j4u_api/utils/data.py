import pandas as pd

from j4u_api.config import config


def get_clean_jobs_df():
    df = pd.read_json(config.JOBS_JSON_PATH)
    df.columns = [x.lower() for x in df.columns]
    df = df.rename(columns={"iscotitle": "isco_title"})
    df = df.drop_duplicates()
    return df


def prepare_jobs():
    df = get_clean_jobs_df()
    records = df.to_dict("records")
    choices_dict = dict(enumerate(df["title"].values))

    return records, choices_dict
