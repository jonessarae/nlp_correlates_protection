"""
This script is designed for identifying publications relevant to the topic of correlates of protection and extracting entities of the following categories:
 - animals
 - assays
 - immune correlates
 - vaccines

To use:
python run_pipeline.py -input <path/to/file> --output <path/to/folder> [options]

Example:
python run_pipeline.py -input isearch_test.xlsx --output results

Parameters:
Required:
-input: path to publication file (iSearch excel file)
Optional:
--output: path to result folder
Other:
-h, --help: help message

Files that are generated:

covid_relevant_abstracts_<date>.xlsx: excel file of COVID-19 publication data identified as relevant by classifier

covid_relevant_abstracts_processed_<date>.xlsx: excel file of relevant processed COVID-19 publication data for Tableau

entities_<date>.xlsx: excel file with entities from customized NER model

entities_with_categories_<date>.xlsx: excel file with entities and their categories
"""
import os
import argparse
import pandas as pd
import pipeline_scripts.classifier as clf
import pipeline_scripts.ner as ner
import pipeline_scripts.prepare_isearch_data as prep
import pipeline_scripts.clean_animal_entities as cln_animal
import pipeline_scripts.clean_correlate_entities as cln_correlate
import pipeline_scripts.clean_assay_entities as cln_assay
import pipeline_scripts.clean_vaccine_entities as cln_vaccine
import warnings
from datetime import datetime
import sys

warnings.filterwarnings("ignore")

# to suppress SettingWithCopyWarning
#pd.options.mode.chained_assignment = None  # default='warn'

def main(args):

    ############## Load data ##############

    # get start time
    start = datetime.now()
    # get date to add to file names
    date = datetime.now().date().strftime("%Y%m%d")

    print("Loading data...", flush = True)

    # get path to publicaton file
    pub_file = args.input

    if args.output:
        # get path to result folder
        directory = args.output
        # if result folder doesn't exit, create folder
        if not os.path.exists(directory):
            os.makedirs(directory)
    else:
        # use current directory
        directory = os.getcwd()

    # read in excel file
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        try:
            df = pd.read_excel(pub_file)
            if "System ID" not in df.columns:
                sys.exit("This is not an iSearch file. Exiting...")
        except Exception as e:
            print(e)
            sys.exit("Exiting...")

    print("Number of publications is {}.".format(df.shape[0]), flush = True)

    ############## Run classifier ##############
    print("Running classifier...")

    # prepare text
    df = clf.prepare_text(df)

    # get relevant publications
    relevant_df = clf.get_relevant_articles(df)

    print("Number of relevant publications is {}.".format(relevant_df.shape[0]), flush = True)

    # check if there are relevant abstracts, if not end pipeline
    if relevant_df.shape[0] > 0:
        print("Saving file...", flush = True)
        # save as excel file (check if output folder and/or prefix)
        relevant_df.to_excel(os.path.join(directory, "covid_relevant_abstracts_{}.xlsx".format(date)), index=False)
    else:
        print("No relevant abstracts found.", flush = True)
        print("Exiting...")

    ############## Prepare data for dashboard ##############

    print("Preparing data for dashboard...", flush = True)

    # process data
    processed_df = prep.process_data(relevant_df)

    print("Saving file...", flush = True)

    # save to excel file
    processed_df.to_excel(os.path.join(directory,"covid_relevant_abstracts_processed_{}.xlsx".format(date)), index = False, na_rep="")

    ############## Run customized NER model ##############

    print("Running NER model...", flush = True)

    # get entities from each abstract
    entity_df = ner.get_entities(processed_df)

    print("Saving file...", flush = True)

    # save to excel file
    entity_df.to_excel(os.path.join(directory,"entities_{}.xlsx".format(date)), index=False)

    ############## Clean entities ##############

    print("Cleaning entities...", flush = True)

    animal_df = cln_animal.clean_ents(entity_df)
    print("Animals are categorized.", flush = True)

    assay_df = cln_assay.clean_ents(entity_df)
    print("Assays are categorized.", flush = True)

    correlate_df = cln_correlate.clean_ents(entity_df)
    print("Correlates are categorized.", flush = True)

    # file of vaccine info
    vaccine_file = "data/COVID_19_Tracker_Vaccines_01262021.csv"
    # create dictionary of vaccine info file
    vaccine_dict = cln_vaccine.make_vaccine_dict(vaccine_file)
    vaccine_df = cln_vaccine.clean_ents(entity_df, vaccine_dict)
    print("Vaccines are categorized.", flush = True)

    # combine all categorized entities
    all_final_ents_df = pd.concat([animal_df, assay_df, correlate_df, vaccine_df])

    print("Saving file...", flush = True)

    # save to excel file
    all_final_ents_df.to_excel(os.path.join(directory,"entities_with_categories_{}.xlsx".format(date)), index=False)

    print("All files saved in: {}".format(os.path.abspath(directory)), flush = True)

    # get time it took to run program
    print("Finished in {}".format(datetime.now()-start))

if __name__ == "__main__":

    # create arguments
    p = argparse.ArgumentParser(description=__doc__, prog = "run_pipeline.py",
        usage = "%(prog)s -input <path/to/file> -output <path/to/folder> -vaccine <path/to/file> --prefix <string> [options]", add_help=True)
    p.add_argument("-input", help="publication file", required=True)
    p.add_argument("--output", help="result folder")
    #p.add_argument("-vaccine", help="path to vaccine info file", required=True)

    # parse arguments
    args = p.parse_args()

    # run program with arguments
    main(args)
