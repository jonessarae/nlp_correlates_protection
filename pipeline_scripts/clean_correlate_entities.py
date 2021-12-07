"""
Categorizing the correlate entities from the custom NER model.
"""
import numpy as np
import pandas as pd
import re

def clean_ents(df):
    """
    Filtering entity output doc to only include correlate entities and categorizing entities.

    Input: df (dataframe) - uncategorized entities
    Returns: correlate_final (dataframe) - categorized entities
    """

    correlate_ents = df[df.Class=='correlate']
    correlate_ents['unique_num'] = correlate_ents.reset_index().index

    table4 = {'System_ID':[], 'unique_num': [], 'Entity':[], 'Category':[]}

    '''Regex rules for categorization'''

    humoral = [r'[Hh]umoral']
    cellular = [r'[Cc]ellular immunity|[Cc]ell-mediated|[Cc]ellular [Ii]mmune|[Cc]ellular|[Cc]ell [Ii]mmune|[Cc]ell [Rr]esponse']
    T_cells = [r'(?<![A-Za-z])T(?![A-Za-z])|[Tt]-cell(s)?|(?<![A-Za-z])[Tt](?![A-Za-z]) cell(s)?(?![Ll]ines)|[Cc][Dd]3+|(?<![A-Za-z])[Tt][Hh](s)?(?![A-Za-z])|(?<![A-Za-z])[Tt][Cc][Rr](s)?(?![A-Za-z])']
    B_cells = [r'(?<![A-Za-z])B(?![A-Za-z])|[Bb]-cell(s)?|[Bb] cell(s)?|(?<![A-Za-z])[Bb][Cc][Rr](s)?(?![A-Za-z])']
    CD4 = [r'[Cc][Dd]4|[Cc][Dd]4+|[Hh]elper|[Tt][Hh]1|[Tt][Hh]2|[Tt][Ff][Hh]']
    CD8 = [r'[Cc][Dd]8|[Cc][Dd]8+|[Cc]ytotoxic|(?<![A-Za-z])[Tt][Cc](?![A-Za-z])|(?<![A-Za-z])[Cc][Tt][Ll](s)?(?![A-Za-z])']
    Memory_response = [r'[Mm]emory']
    antibodies = [r'[Aa]ntibodies|[Aa]ntibody|[Aa][Bb](s)?|CR\d|CD\d|CV\d|CD107a|H\d{1}|H-2|[Aa]nti-[A-Za-z]{0,3}\d{0,2}(?![Ii]nflammatory)']
    neutralizing = [r'[Nn]eutrali[zs]ing|[Nn]eutrali[zs]ation|[Nn][Aa][bB](s)?']
    immunoglobulins = [r'[Ii]mmunoglobulin(s)?|(?<![A-Za-z])[Ii][Gg](s)?(?![A-Za-z])|(?<![A-Za-z])[Ii][Gg][a-zA-Z]{1}(?![A-Za-z])|(?<![A-Za-z])Ig(?![A-Za-z])']
    IgA = [r'[Ii][Gg][Aa]|[Ii][Gg] [Aa]']
    IgG = [r'[Ii][Gg][Gg]|[Ii][Gg] [Gg]']
    IgE = [r'[Ii][Gg][Ee]|[Ii][Gg] [Ee]']
    IgM = [r'[Ii][Gg][Mm]|[Ii][Gg] [Mm]']
    lymphocytes = [r'[Ll]ymphocyte(s)?']
    other_titers = [r'[Tt]iter(s)?|[Gg]eometric [Mm]ean [Tt]iter(s)?|[Gg][Mm][Tt](s)?|[Tt]itre(s)?|[Rr]eciprocal [Tt]iter(s)?|[Bb]inding [Ll]evels']
    other_cells = [r'NK cell(s)?|NK-cell(s)?|NK|[Cc]yotokine(s)?|[Ee]ffector [Cc]ell(s)?|[Pp]eripheral [Mm]yeloid [Cc]ells|(?<![Cc]ell-)[Cc]ell(s)?(?!-cell)|[Bb]asophil']
    other_immune_response = [r'[Pp]rotective [Ii]mmunity|[Ii]mmune [Rr]esponse|[Ii]mmunity|[Ii]mmune [Pp]rotection|[Pp]olyclonal|[Rr]esponse(s)?']
    misclassified = [r'[Vv]accine|[Vv]accination|[Aa]ssay(s)?|[Mm]ice|[Mm]ouse|[Hh]amster(s)|ELISA|[Ff]low-[Cc]ytometry|[Ff]low [Cc]ytometry|SARS-CoV/macaque']
    falsePos = [r'[Ii]nflammation|SARS-CoV-2 infection|SARS-C[Oo]V-2|SARS-CoV2|SARS-C[Oo]V']

    for index, row in correlate_ents.iterrows():
        sys_id = correlate_ents.loc[index, 'System_ID']
        entity = correlate_ents.loc[index, 'Entity']
        animal = correlate_ents.loc[index, 'Class']
        uniq_id = correlate_ents.loc[index, 'unique_num']
        for pattern in Memory_response:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('Memory response')
        for pattern in CD4:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('CD4 cells')
        for pattern in CD8:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('CD8 cells')
        for pattern in neutralizing:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('neutralizing response')
        for pattern in IgA:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('IgA')
        for pattern in IgG:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('IgG')
        for pattern in IgE:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('IgE')
        for pattern in IgM:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('IgM')
        for pattern in immunoglobulins:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('immunoglobulins')
        for pattern in humoral:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('humoral immunity')
        for pattern in cellular:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('cellular immunity')
        for pattern in T_cells:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('T cells')
        for pattern in B_cells:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('B cells')
        for pattern in misclassified:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('misclassified')
        for pattern in antibodies:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('antibodies')
        for pattern in lymphocytes:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('lymphocytes')
        for pattern in other_cells:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('other cells')
        for pattern in other_titers:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('other immune titers')
        for pattern in other_immune_response:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('other immune responses')
        for pattern in falsePos:
            if re.findall(pattern, entity):
                table4['System_ID'].append(sys_id)
                table4['unique_num'].append(uniq_id)
                table4['Entity'].append(entity)
                table4['Category'].append('false positive')

    '''
    The for loop is set up from more specific to less specific categories, so the entities get their most specific category assigned first;
    This allows us to drop the duplicated categories after the first one, keeping the most relevant
    '''
    corr_cats = pd.DataFrame(table4)
    nodups_cats = corr_cats.drop_duplicates(subset=['unique_num'], keep='first')

    '''Filtering out all entities that were not categorized and labeling as false positives'''
    check4 = correlate_ents[~correlate_ents['unique_num'].isin(nodups_cats['unique_num'])]
    check4["Category"] = 'false positive'

    '''Concatenating categorized DataFrames and only keeping needed columns'''
    corr_concat = pd.concat([nodups_cats, check4])
    corr_concat = corr_concat[['System_ID', 'Entity', 'Category']]

    correlate_final = correlate_ents.merge(corr_concat, on=['System_ID', 'Entity'], how='left')
    correlate_final = correlate_final[['System_ID', 'Doc', 'Entity', 'Category','Class']]

    return(correlate_final)
