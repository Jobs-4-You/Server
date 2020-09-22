import warnings
from collections import Counter

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform

from j4u_api.config import config
from j4u_api.utils.data import get_clean_jobs_df

warnings.filterwarnings("ignore")


class Engine:
    def __init__(self):
        data = pd.read_csv(config.ONET_CSV_PATH, encoding="latin1")
        codes = set(data["isco08"].values)
        code_to_title = {
            c: data[data["isco08"] == c]["TitreFR"].values[0] for c in codes
        }
        # Read the Data

        # Rename the column TitreFR to Occupation
        # data.rename(columns = {'TitreFR' : 'Occupation'}, inplace = True)
        data["Occupation"] = data["isco08"]

        # Drop the useless columns
        data.drop(columns=[u"ElementID", u"isco08"], inplace=True)

        # Set the occupation name as index of the dataFrame
        data.set_index("Occupation", inplace=True)

        # Drop the 'Membres des corps législatifs' job
        # data.drop(u'Membres des corps législatifs', inplace = True)

        # Replce the missing ElementName of the 'JobZones' Domain
        data["ElementName"] = data["ElementName"].fillna(value="JobZones")

        # Drop the missing rows from ElementName
        data.dropna(subset=[u"ElementName"], inplace=True)
        self.data = data
        self.code_to_title = code_to_title
        self.jobs = get_clean_jobs_df()

    def compute_dist(self, quest_point, past_occup, alpha, beta):
        print(alpha, beta, "--")
        domains = pd.unique(self.data["Domain"])

        # Create a dictionary that will contain the df of the different domains
        dfs = {}
        for domain in domains:
            dfs[domain] = self.data.loc[self.data["Domain"] == domain]

        # Create the new rows of the dataFrame for the questionnaire
        questionnaire_df = dfs[u"MM"].copy().reset_index().iloc[:12]
        questionnaire_df["Occupation"] = u"Questionnaire"
        questionnaire_df["DataValue"] = quest_point
        questionnaire_df.set_index("Occupation", inplace=True)
        dfs[u"MM"] = dfs[u"MM"].append(questionnaire_df)

        distance_dfs = {}

        for domain in dfs.keys():

            # Get the DataFrame of the current Domain
            df = dfs[domain].copy()
            # Drop the useless Columns and reset the index
            df.drop(columns=["ElementName", "Domain"], inplace=True)
            df.reset_index(inplace=True)

            # Create the new index on which we will pivot the dataFrame
            nb_elem_byOccup = len(df.loc[df["Occupation"] == df["Occupation"][0]])
            nb_occupations = len(pd.unique(df["Occupation"]))
            df["new_index"] = list(range(nb_elem_byOccup)) * nb_occupations

            # Pivot the DataFrame such that we have the occupation on the columns
            df = df.pivot(index="new_index", columns="Occupation", values="DataValue").T

            # Compute the normalized pairwise distance between the occupations
            dist_df = pd.DataFrame(
                squareform(pdist(df, "euclidean")), index=df.index, columns=df.index
            )

            # If domain is MM normalize later
            if not (domain == u"MM"):
                dist_df = (dist_df - np.mean(dist_df.values)) / np.std(dist_df.values)

            distance_dfs[domain] = dist_df

        # Sum of values for all pairwise Occupations of all the domains except MM
        sum_domains = sum(
            [distance_dfs[domain] for domain in domains if not domain == u"MM"]
        )

        # Sum of values for all pairwise Occupations of the MM domain and drop the row and column questionnaire
        D_mmP = distance_dfs[u"MM"]
        D_mmP = D_mmP.drop(["Questionnaire"]).drop(columns=["Questionnaire"])
        D_mmP = (D_mmP - np.mean(D_mmP.values)) / np.std(D_mmP.values)

        # Sum of values for all Occupations of the MM domain to the questionnaire values
        D_mmS = distance_dfs[u"MM"].loc["Questionnaire"].copy()
        del D_mmS["Questionnaire"]
        D_mmS = (D_mmS - np.mean(D_mmS)) / np.std(D_mmS)

        final_dist = (
            alpha * D_mmS
            + (1 - alpha) * D_mmP[past_occup]
            + beta * sum_domains[past_occup]
        ) / (1 + beta * 9)
        final_dist = final_dist.sort_values()

        return list(final_dist.index)[:20], np.round(final_dist.values, 3)

    def recom(self, *var):
        # Slider values from 1 to 5
        list_var = [
            var[0],
            var[1],
            var[2],
            var[3],
            var[4],
            var[5],
            var[6],
            var[7],
            var[8],
            var[9],
            var[10],
            var[11],
        ]
        # The weight Importance of the old Position values
        weight_oldPos_alpha = var[12]  # / 100

        abilitiesImportance_beta = var[14]  # / 100

        oldPos = var[13]

        # Return the list of jobs that are the closest to the parameters we did input
        res = self.compute_dist(
            list_var, oldPos, weight_oldPos_alpha, abilitiesImportance_beta
        )

        isco08_list = list(res[0])
        job_title_list = []
        avam_list = []
        bfs_list = []
        df = self.jobs
        for cc in isco08_list:
            matches = df.loc[df["isco08"] == cc]
            avams = matches["avam"].values.tolist()
            bfss = matches["bfs"].values.tolist()
            job_titles = matches["title"].values.tolist()

            avam_list += avams
            bfs_list += bfss
            job_title_list += job_titles

        return {
            "var_list": list_var,
            "isco08_list": isco08_list,
            "job_title_list": job_title_list,
            "avam_list": avam_list,
            "bfs_list": bfs_list,
            "importances": list(res[1]),
        }
