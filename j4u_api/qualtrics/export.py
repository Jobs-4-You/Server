import io
import zipfile
from io import StringIO

import pandas as pd
import requests


def export(token, data_center, survey_id):
    # Setting static parameters
    requestCheckProgress = 0.0
    progressStatus = "inProgress"
    url = f"https://{data_center}.qualtrics.com/API/v3/surveys/{survey_id}/export-responses/"
    headers = {
        "content-type": "application/json",
        "x-api-token": token,
    }

    # Step 1: Creating Data Export
    data = {"format": "csv", "seenUnansweredRecode": 2}

    downloadRequestResponse = requests.request("POST", url, json=data, headers=headers)

    progressId = downloadRequestResponse.json()["result"]["progressId"]

    isFile = None

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while (
        progressStatus != "complete" and progressStatus != "failed" and isFile is None
    ):
        requestCheckUrl = url + progressId
        requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
        try:
            isFile = requestCheckResponse.json()["result"]["fileId"]
        except KeyError:
            1 == 1
        requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
        progressStatus = requestCheckResponse.json()["result"]["status"]

    # step 2.1: Check for error
    if progressStatus == "failed":
        raise Exception("export failed")

    fileId = requestCheckResponse.json()["result"]["fileId"]

    # Step 3: Downloading file
    requestDownloadUrl = url + fileId + "/file"
    requestDownload = requests.request(
        "GET", requestDownloadUrl, headers=headers, stream=True
    )

    # Step 4: Unzipping the file
    z = zipfile.ZipFile(io.BytesIO(requestDownload.content))
    name = z.namelist()[0]
    data = z.read(name)
    return pd.read_csv(StringIO(str(data, "utf-8")))
