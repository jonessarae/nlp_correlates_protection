"""
Categorizing the vaccine entities from the custom NER model.
"""
import numpy as np
import pandas as pd
import re
import numpy as np
from fuzzywuzzy import fuzz, process

def clean_ents(df, vaccine_dict):
    """
    Filtering entity output doc to only include vaccine entities and categorize entities.

    Input: df (dataframe) - uncategorized entities
           vaccine_dict (dictionary) - vaccine info from Milken Institute
    Returns: vaccine_final (dataframe) - categorized entities
    """

    # filter to vaccine entities
    vaccine_ents = df[df.Class == "vaccine"]

    """Subset data based on whether entity includes vaccine or candidate"""

    # subset entities to those that contain vaccine or candidate
    vaccine_ent_subset = vaccine_ents[vaccine_ents.Entity.str.contains("vaccin|candidat", case=False)]

    # subset entities that do not contain vaccine term
    vaccine_ent_no_vaccine = vaccine_ents[~vaccine_ents.Entity.str.contains("vaccin|candidat", case=False)]

    """Further subset data if entity contains terms other than COVID-19"""

    # subset entities that contain only COVID-19 or SARS-CoV-2 and vaccine
    vaccine_ent_subset_covid = vaccine_ent_subset[vaccine_ent_subset.Entity.str.
                           contains("^(.*coronavirus|covid-19|sars-cov-2|sars)\s(vaccin*).*", case=False)]

    # subset entities that mention only vaccine candidate or candidate vaccine
    vaccine_ent_candidate = vaccine_ent_subset[vaccine_ent_subset.Entity.str.
                        contains("^(vaccin.*)\s(candidat.*)|^(candidat.*)", case=False)]

    # combine dataframes as one
    vaccine_ent_covid_only = pd.concat([vaccine_ent_subset_covid,       vaccine_ent_candidate])

    # add column for category
    vaccine_ent_covid_only["Category"] = "general covid-19 vaccine"

    # subset entities that contain additional words along with COVID-19 or SARS-CoV-2 and vaccine
    vaccine_ent_other = vaccine_ent_subset[~vaccine_ent_subset.Entity.str.
                              contains("^(.*coronavirus|covid-19|sars-cov-2|sars)\s(vaccin.*).*", case=False)]

    # remove entities that mention only vaccine candidate
    vaccine_ent_other = vaccine_ent_other[~vaccine_ent_other.Entity.str.
                              contains("^(vaccin.*)\s(candidat.*)", case=False)]

    """Use FuzzyWuzzy for entities containing vaccine and terms besides COVID-19"""

    # list of COVID-19 related terms
    covid_list = ["ncov19","nco-19","covid19","covid-19","sars-cov-2","cov2","cov","sars-cov"]

    # go through each row in dataframe
    for index, row in vaccine_ent_other.iterrows():
        # get entity
        entity = vaccine_ent_other.loc[index, "Entity"]
        # get list of matching patterns - first group is anything preceding vaccine or candidate
        entity_sub = re.findall('(.*)(\s|-)(vaccin.*|candidat*).*', entity.lower())
        # if length of list is 0
        if len(entity_sub) == 0:
            # if entity contains COVID-19-related terms
            if any(ele in entity.lower() for ele in covid_list):
                # classify as general COVID-19 vaccine
                vaccine_ent_other.loc[index, "Category"] = "general COVID-19 vaccine"
            else:
                # classify as non-specific vaccine
                vaccine_ent_other.loc[index, "Category"] = "non-specific vaccine"
        # if entity group is empty string, indicates it didn't match patterns
        elif entity_sub[0][0] is " ":
            # classify as non-specific vaccine
            vaccine_ent_other.loc[index, "Category"] = "non-specific vaccine"
        else:
            # dictionary to hold scores for vaccine categories
            scores = dict()
            # iterate through dictionary vaccine types
            for vaccine, vaccine_products in vaccine_dict.items():
                # get best score for each vaccine type
                best_ratio = process.extractOne(entity_sub[0][0], vaccine_products, scorer=fuzz.token_set_ratio)
                # store score
                scores[vaccine] = best_ratio[1]
            # get category with max score
            max_category = max(scores, key=scores.get)
            # get max score
            max_score = max(scores.values())
            # if max score above threshold
            if max_score >= 65:
                # save category as vaccine type
                vaccine_ent_other.loc[index, "Category"] = max_category
            else:
                # classify as non-specific vaccine
                vaccine_ent_other.loc[index, "Category"] = "non-specific vaccine"

    """Use FuzzyWuzzy for entities without vaccine term"""

    # go through each row in dataframe
    for index, row in vaccine_ent_no_vaccine.iterrows():
        # get entity
        entity = vaccine_ent_no_vaccine.loc[index, "Entity"]
        # dictionary to hold scores for vaccine categories
        scores = dict()
        # iterate through dictionary vaccine types
        for vaccine, vaccine_products in vaccine_dict.items():
            # get best score for each vaccine type
            best_ratio = process.extractOne(entity, vaccine_products, scorer=fuzz.token_set_ratio)
            # store score
            scores[vaccine] = best_ratio[1]
        # get category with max score
        max_category = max(scores, key=scores.get)
        # get max score
        max_score = max(scores.values())
        # if max score above threshold
        if max_score >= 65:
            # save category as vaccine type
            vaccine_ent_no_vaccine.loc[index, "Category"] = max_category
        else:
            # else label as false positive
            vaccine_ent_no_vaccine.loc[index, "Category"] = "false positive"

    # combine all dataframes
    vaccine_final = pd.concat([vaccine_ent_covid_only,
                                 vaccine_ent_other,
                                 vaccine_ent_no_vaccine])

    return vaccine_final

def make_vaccine_dict(vaccine_file):
    """
    Create vaccine dictionary from vaccine info file from Milken Institute with keys as Product Category and values as Product Description.

    Input: vaccine_file (string) - COVID-19 vaccine info
    Returns: vaccine_dict (dictionary)
    """
    # read in file
    vaccines = pd.read_csv(vaccine_file)

    # keep only product category and product description
    vaccine_info = vaccines[["Product Category", "Product Description"]].drop_duplicates()

    # rename columns
    vaccine_info = vaccine_info.rename(columns={"Product Category": "Category", "Product Description": "Product"})

    # get list of products for each vaccine type
    unknown = vaccine_info[vaccine_info.Category=="Unknown"].Product.tolist()

    replicating_bacterial_vector = vaccine_info[vaccine_info.Category=="Replicating bacterial vector"].Product.tolist()

    live_attenuated_virus = vaccine_info[vaccine_info.Category=="Live attenuated virus"].Product.tolist()

    dna_based_vaccine = vaccine_info[vaccine_info.Category=="DNA-based"].Product.tolist()

    rna_based_vaccine = vaccine_info[vaccine_info.Category=="RNA-based vaccine"].Product.tolist()

    inactivated_virus = vaccine_info[vaccine_info.Category=="Inactivated virus"].Product.tolist()

    virus_like_particle = vaccine_info[vaccine_info.Category=="Virus-like particle"].Product.tolist()

    protein_subunit = vaccine_info[vaccine_info.Category=="Protein subunit"].Product.tolist()

    replicating_viral_vector = vaccine_info[vaccine_info.Category=="Replicating viral vector"].Product.tolist()

    non_replicating_viral_vector = vaccine_info[vaccine_info.Category=="Non-replicating viral vector"].Product.tolist()

    # make dictionary of vaccine types
    vaccine_dict = {"replicating bacterial vector": replicating_bacterial_vector,
                "live-attenuated virus": live_attenuated_virus,
                "dna-based vaccine": dna_based_vaccine,
                "rna-based vaccine": rna_based_vaccine,
                "inactivated virus": inactivated_virus,
                "virus-like particle": virus_like_particle,
                "protein subunit": protein_subunit,
                "replicating viral vector": replicating_viral_vector,
                "non-replicating viral vector": non_replicating_viral_vector,
                "not classified": unknown}

    return vaccine_dict
