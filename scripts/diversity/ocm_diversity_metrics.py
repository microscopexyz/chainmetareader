#!/usr/bin/env python3

# Copyright 2023 The chainmetareader Authors. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pandas as pd


def entropy_calc(x_dist):
    """
    Takes in probability and calculates the entropy value
    Args:
        x_dist: numpy array which is a float vlaue array
    Returns: entropy for distribution x
    """
    return -x_dist * np.log(x_dist)


def calc_diversity_metircs(ocm_count_by_entity_csv_file):
    """
    Takes in probability and calculates the entropy value
    Args:
        x_dist: numpy array which is a float vlaue array
    Returns:
        top_3: Categories Concentratio of OCM entities who contribute the labeled data
        gini_coefficient: Gini coefficient: of OCM entities who contribute the labeled data
        shannon_entropy: Shannon entropy of OCM entities who contribute the labeled data
    """
    data_frame = pd.read_csv(ocm_count_by_entity_csv_file)
    top_3_df = data_frame.sort_values(by=["percentage_of_total"], ascending=False).head(
        3
    )
    top_3 = top_3_df["percentage_of_total"].sum()

    # Sort the DataFrame by percentage_of_total in descending order
    data_frame = data_frame.sort_values(by="percentage_of_total", ascending=False)

    # Calculate the cumulative sum of the percentage_of_total column
    data_frame["cumulative_percentage"] = data_frame["percentage_of_total"].cumsum()

    # Calculate the proportion of total and cumulative proportion of tags
    data_frame["proportion_of_total"] = (
        data_frame["percentage_of_total"] / data_frame["percentage_of_total"].sum()
    )
    data_frame["cumulative_proportion"] = (
        data_frame["cumulative_percentage"] / data_frame["percentage_of_total"].sum()
    )

    # Calculate the Lorenz curve; represents the cumulative proportion of
    # the total on the y-axis and the cumulative proportion of tags on the x-axis
    data_frame["lorenz_curve"] = data_frame["cumulative_proportion"]

    # Calculate the area under the Lorenz curve
    area_lorenz = data_frame["lorenz_curve"].sum() / len(data_frame)

    # Calculate the area of the perfect equality line
    area_perfect_equality = 0.5

    # Calculate the Gini coefficient
    gini_coefficient = abs(
        (area_perfect_equality - area_lorenz) / area_perfect_equality
    )

    shannon_df = data_frame.copy()

    # create entropy column by calling the entropy_calc() function
    # on the proportion_of_total column which represents 'probability'
    shannon_df["entropy"] = shannon_df["proportion_of_total"].apply(entropy_calc)

    # sum the entropy column to get the Shannon entropy value
    shannon_entropy = shannon_df["entropy"].sum()

    return top_3, gini_coefficient, shannon_entropy


COUNT_BY_ENTITY_CSV = "ocm_count_by_entity.csv"
metric_top_3, metric_gini_coefficient, metric_shannon_entropy = calc_diversity_metircs(
    COUNT_BY_ENTITY_CSV
)

print("Top 3 Categories Concentration: ", metric_top_3)
print("Gini coefficient:", metric_gini_coefficient)
print("Shannon entropy:", metric_shannon_entropy)
