"""
Purpose: Identify articles that are relevant to the topic of immune correlates of protection.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import numpy as np
import pickle
import pandas as pd
import os

def clean_str(string):
    """
    Tokenization/string cleaning of text.

    Original code from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`\-]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    #return string.strip().lower()
    return string.strip()

def prepare_text(df):
    """
    Clean text and concatenate title and abstract.

    Input: df (dataframe) - iSearch publication data
    Returns: df (dataframe)
    """
    # concatenate title and abstract
    df["Text"] = df["Title"] + ". " + df["Abstract"]
    # clean text
    df["cleaned_text"] = df["Text"].apply(lambda x: clean_str(str(x)))

    return df

def get_relevant_articles(df):
    """
    Identify relevant articles using classifier.

    Input: df (dataframe) - iSearch publication data
    Returns: relevant_df (dataframe)
    """
    # load the model and TFIDF vectorizer
    model_filename = "sgd_l2.pkl"
    tfidf_filename = "tfidf.pkl"
    model_folder = "models/classifier"
    sgd_classifier = pickle.load(open(os.path.join(model_folder, model_filename), "rb"))
    tfidfvectorizer = pickle.load(open(os.path.join(model_folder, tfidf_filename), "rb"))

    # encode text
    encoded_text = tfidfvectorizer.transform(df["cleaned_text"].values)
    # get predicted labels
    predictions = sgd_classifier.predict(encoded_text)
    # get probabilities
    probabilities = sgd_classifier.predict_proba(encoded_text)
    # keep only the max probability for each publication
    max_probs = np.amax(probabilities, axis=1)

    # add predictions to dataframe of publication info
    df["prediction"] = predictions
    df["probability"] = max_probs
    # drop unneeded column
    df = df.drop("cleaned_text", axis=1)

    # filter to just positive labels
    relevant_df = df[df.prediction == 1]

    return relevant_df
