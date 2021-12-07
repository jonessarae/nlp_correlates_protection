"""
Purpose: Prepare iSearch results for dashboard.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import numpy as np
import pickle
import pandas as pd
import os

def make_hyperlink(prefix, value):
    """
    Make hyperlink.
    Input: prefix (string) - name of website
           value (string) - unique identifier to added to prefix
    Returns: hyperlink (sting)
    """
    prefix = prefix
    # combine prefix and value as url
    url = prefix + str(value)

    return '=HYPERLINK("%s", "%s")' % (url.format(value), value)

def process_data(df):
    """
    Clean abstracts and extract and prepare hyperlinks for the following:
    - ClinicalTrials.gov NCT number
    - DOIs
    - PMIDs

    Input: df (dataframe)
    Returns: df (dataframe)
    """
    # replace spaces with underscores in column names
    new_cols = df.columns.str.replace("\s+", "_")
    df.columns = new_cols

    # remove trailing white spaces
    df["Abstract"] = df["Abstract"].apply(lambda x: x.strip())

    # remove line breaks
    df["Abstract"] = df["Abstract"].apply(lambda x: x.replace("\n"," "))

    # extract clinical trial id
    df["Clinical_Trial_ID"] = df["Abstract"].str.extract(r"(NCT[0-9]*)")

    # make column with hyperlink to trial
    df["Link_to_trial"] = df["Clinical_Trial_ID"].apply(lambda x: make_hyperlink("https://clinicaltrials.gov/show/", x) if "NCT" in str(x) else np.nan)

    # make column with hyperlink for DOIs
    df["Link_to_DOI"] = df["DOI"].apply(lambda x: make_hyperlink("https://doi.org/", x) if "/" in str(x) else np.nan)

    # convert PMID column from float to string type
    df["PMID"] = df["PMID"].astype(str).replace("\.0", "", regex=True)

    # make column with hyperlink for PMIDs
    df["Link_to_PubMed"] = df["PMID"].apply(lambda x: make_hyperlink("https://www.ncbi.nlm.nih.gov/pubmed/", x) if x.isdigit() else np.nan)

    return df
