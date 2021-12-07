"""
Loading the custom NER model and running output from the classifier through it.
"""

import numpy as np
import pandas as pd
import spacy
import os

def get_entities(df):
    """
    Run NER model and get entities.

    Input: df (dataframe) - contains relevant abstracts
    Returns: entity_df (dataframe) - entities found in abstracts
    """
    # path to NER model
    ner_model_dir = "models/ner/Base_NER"

    print("Loading NER model from", ner_model_dir)

    # load model
    nlp = spacy.load(ner_model_dir)

    # shows all pipe names for loaded model
    print("Model pipe names:", nlp.pipe_names)

    # select columns needed - System_ID is unique identifier from iSearch
    df = df[["System_ID", "Text"]]

    '''Clean text'''
    # remove trailing white spaces
    df["Text"] = df["Text"].apply(lambda x: x.strip())
    # remove line breaks
    df["Text"] = df["Text"].apply(lambda x: x.replace("\n"," "))

    # create table
    table = {"System_ID":[], "Doc":[],"Entity":[], "Class":[]}

    # create index
    df.index

    # loop through each abstract
    for index, row in df.iterrows():
        # get System_ID
        sys_id = df.loc[index, "System_ID"]
        # get Text
        text = df.loc[index, "Text"]
        # skip if text is a float type
        if type(text) == float:
            continue
        # run model on text
        doc = nlp(text)
        # create dictionary to hold entities
        ent_bc = {}
        # get entities and their labels
        for x in doc.ents:
            ent_bc[x.text] = x.label_

        # append values to table
        for key in ent_bc:
            table["System_ID"].append(sys_id)
            table["Doc"].append(doc)
            table["Entity"].append(key)
            table["Class"].append(ent_bc[key])

    # convert table to dateframe
    entity_df = pd.DataFrame(table)

    return entity_df
