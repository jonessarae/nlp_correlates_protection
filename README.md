# NLP Correlates of Protection
Project to identify COVID-19 correlates of protection from abstracts using Natural Language Processing (NLP).

## Team

Sydney Foote

Sara Jones

## Purpose

The purpose of this pipeline is for identifying publications relevant to the topic of correlates of protection and extracting entities of the following categories:
 - animals
 - assays
 - immune correlates
 - vaccines

## To Install

Python (pipeline used 3.7.3) and packages with versions are listed in environment.yml.

### To install with conda

To install with conda, you will need conda version >= 4.6.3 (pipeline used 4.6.3).

To install with environment.yml:

```
conda env create -f environment.yml
```

To install without environment.yml:

```
# add conda-forge channel
conda config --append channels conda-forge

# create environment
conda create -n covid_env python=3.7.3 pandas numpy openpyxl jupyter spacy=2.3.2 scikit-learn=0.23.2 nltk=3.4.4 fuzzywuzzy xlrd python-levenshtein -y

# check for environment
conda info --e

# activate environment
conda activate covid_env

# install scispacy and en_core_sci_lg
pip install scispacy==0.3.0
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.3.0/en_core_sci_lg-0.3.0.tar.gz
```

When finished or no longer need environment, run the following commands:

```
# deactivate environment
conda deactivate

# remove environment
conda env remove --name covid_env
```

### To install with Docker

TO DO

### To install with pip

TO DO

## To Use

This pipeline takes in excel files of publication and preprint data from iSearch COVID-19 portfolio (https://icite.od.nih.gov/covid19/search/) as input.

```
python run_pipeline.py -input <path/to/file> --output <path/to/folder> [options]
```

Example:
```
python run_pipeline.py -input isearch_test.xlsx --output results
```

Parameters:

Required:

*-input*: path to publication file (iSearch excel file)
 
Optional:

 *--output*: path to result folder
 
Other:

 *-h, --help*: help message

Files that are generated:

 - **covid_relevant_abstracts_<date>.xlsx**: excel file of COVID-19 publication data identified as relevant by classifier

 - **covid_relevant_abstracts_processed_<date>.xlsx**: excel file of relevant processed COVID-19 publication data for Tableau or dashboard of choice

 - **entities_<date>.xlsx**: excel file with entities from customized NER model

 - **entities_with_categories_<date>.xlsx**: excel file with entities and their categories for Tableau or dashboard of choice

## Features to add later
 
 - Create a web scraper to pull iSearch records daily or weekly
 - Create a classifier to detect review/editorials 
 - Identify duration of immunity
 - Determine if vaccine has a positive, negative, or neutral effect on identified correlate
 
## License

This project is MIT licensed.
