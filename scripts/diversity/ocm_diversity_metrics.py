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

import pandas as pd
import numpy as np


def entropy_calc(x):
    """Takes in probability and calculates the entropy value"""
    return -x * np.log(x)


def get_diversity_metircs(ocm_count_by_entity_csv_file):
    
    df = pd.read_csv(ocm_count_by_entity_csv_file)
    top_3_df = df.sort_values(by=["percentage_of_total"], ascending=False).head(3)
    top_3 = top_3_df["percentage_of_total"].sum()
    
    # Sort the DataFrame by percentage_of_total in descending order
    df = df.sort_values(by="percentage_of_total", ascending=False)

    # Calculate the cumulative sum of the percentage_of_total column
    df["cumulative_percentage"] = df["percentage_of_total"].cumsum()

    # Calculate the proportion of total and cumulative proportion of tags
    df["proportion_of_total"] = df["percentage_of_total"] / df["percentage_of_total"].sum()
    df["cumulative_proportion"] = df["cumulative_percentage"] / df["percentage_of_total"].sum()

    # Calculate the Lorenz curve; represents the cumulative proportion of the total on the y-axis 
    # and the cumulative proportion of tags on the x-axis
    df["lorenz_curve"] = df["cumulative_proportion"]

    # Calculate the area under the Lorenz curve
    area_lorenz = df["lorenz_curve"].sum() / len(df)

    # Calculate the area of the perfect equality line
    area_perfect_equality = 0.5

    # Calculate the Gini coefficient
    gini_coefficient = abs((area_perfect_equality - area_lorenz) / area_perfect_equality)

    shannon_df = df.copy()

    # create entropy column by calling the entropy_calc() function on the proportion_of_total column 
    # which represents 'probability'
    shannon_df['entropy'] = shannon_df['proportion_of_total'].apply(entropy_calc)

    # sum the entropy column to get the Shannon entropy value
    shannon_entropy = shannon_df['entropy'].sum()
    
    return top_3, gini_coefficient, shannon_entropy


count_by_entity_csv = "ocm_count_by_entity.csv"
top_3, gini_coefficient, shannon_entropy = get_diversity_metircs(count_by_entity_csv)

print("Top 3 Categories Concentration: ", top_3)
print("Gini coefficient:", gini_coefficient)
print("Shannon entropy:", shannon_entropy)