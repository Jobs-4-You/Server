from j4u_api.config import config
from j4u_api.qualtrics import Qualtrics

qualtrics = Qualtrics(config.QUALTRICS_TOKEN, "eu")

qualtrics.list_surveys()
