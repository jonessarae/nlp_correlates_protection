# COVID-19 Correlates of Protection
NLP project to identify COVID-19 correlates of protection from abstracts.



## Table of Contents

## File Directory

<pre>
STUDY
└── READS
    ├── Sample_1
    │   ├── Unaligned reads
    │   └── Aligned.sam/bam
    ├── Sample_2
    │   ├── Unaligned reads
    │   └── Aligned.sam/bam
    ├── Sample_3
    │   ├── Unaligned reads
    │   └── Aligned.sam/bam
    └── Sample_4
        ├── Unaligned reads
        └── Aligned.sam/bam
</pre>


## TO DO

 
 - [ ] Create a web scraper to pull iSearch records daily - use AWS Lambda
 - [ ] Craete a web scraper to pull in latest vaccine data, Milken Institute
 - [ ] Preprocess records:
    - [ ] Clean up text such as removing large whitespaces
    - [ ] Use right encoding to show special characters
    - [ ] Detect non-English or empty abstracts
    - [ ] Get hyperlinks from excel files
 - [x] Create a classifier to find relevant publications and keep if above a certain threshold
 - [ ] Save data in SQLite or CSV?
 - [ ] Create a customized NER model for entities: vaccine, correlate, animal, and assay
 - [ ] Add rules (i.e. identify clincial trials)
 - [ ] Run each relevant publication (specifically non-review publications) through NER model and save identified entities
 - [ ] Create dashboard with Streamlit with the following features:
    - [ ] Filter on publication type
    - [ ] Show NER annotations within text
    - [ ] Sort by date, relevance probability score
    - [ ] Include date when last updated
 - [ ] Use Plotly for charts
    - Plots to generate?

 
 
 Features to add later if we have time
 
 - Create a classifier to detect review/editorials 
 - Include a keyword search
 - Identify duration of immunity
 - Determine if vaccine has a positive, negative, or neutral effect on identified correlate
 - Option to download selected PMIDS as csv


## Acknowledgements
