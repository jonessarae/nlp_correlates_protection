"""
Categorizing the animal entities from the custom NER model.
"""
import numpy as np
import pandas as pd
import re

def clean_ents(df):
    """
    Filtering entity output doc to only include animal entities and categorizing entities.

    Input: df (dataframe) - uncategorized entities
    Returns: animal_final (dataframe) - categorized entities
    """
    animal_ents = df[df.Class == 'animal']
    animal_ents['unique_num'] = animal_ents.reset_index().index

    table = {'System_ID':[], 'unique_num': [], 'Entity':[], 'Category':[]}

    '''Regex rules for categorization'''

    human = [r'(?<![Nn]on )[Hh]uman(s)?$(?! [Pp]rimate(s)?)']
    mouse = [r'[Mm]ouse|[Mm]ice|[Rr]at(s)?|murine|BALB/c']
    hamster = [r'[Hh]amster[s]?']
    nhp = [r'rhesus|[Mm]acaques?|[Pp]rimate[s]?(?! [Mm]ammal(s)?)|Macaca|chimpanzee[s]?|marmoset[s]?|[Mm]onkey|[Bb]aboon(s)?|NHP(s)?|ape(s)?|[Gg]orilla(s)?|fascicularis']
    ferret = [r'[Ff]erret(s)?']
    gpig = ['[Gg]uinea']
    pig = [r'(?<![Gg]uinea )[Pp]ig[s]?|piglet']
    bat = [r'[Bb]at[s]?']
    cat = [r'[Cc]at[s]?(?!tle)']
    dog = [r'[Dd]og[s]?|puppy|puppies']
    cow = [r'[Cc]ow[s]?|calve[s]?|[Cc]attle']
    rabbit = [r'[Rr]abbit[s]?|[Hh]are(s)?']
    llama = [r'[Ll]lama[s]?']
    camel = [r'[Cc]amel[s]?|[Dd]romedaries|[Dd]romedary']
    porcupine = [r'porcupine[s]?|porcine']
    chicken = [r'chick[s]?|bird[s]?']
    other = [r'non-rodent(s)|rodent(s)?|mammal(s)?|zebrafish[es]?|[Tt]ortoise(s)?|[Mm]armot(s)?']
    misclassified = [r'humanized”\) antibodies|non-competing mAb|NtAb assay|non-functional T cells|non-standardized neutralizing assays|non-functional ELISA assays|CoV2pp']

    for index, row in animal_ents.iterrows():
        sys_id = animal_ents.loc[index, 'System_ID']
        entity = animal_ents.loc[index, 'Entity']
        animal = animal_ents.loc[index, 'Class']
        uniq_id = animal_ents.loc[index, 'unique_num']
        for pattern in human:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('human')
        for pattern in mouse:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('mouse')
        for pattern in hamster:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('hamster')
        for pattern in nhp:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('non-human primate')
        for pattern in ferret:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('ferret')
        for pattern in gpig:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('guinea pig')
        for pattern in pig:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('pig')
        for pattern in bat:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('bat')
        for pattern in cat:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('cat')
        for pattern in dog:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('dog')
        for pattern in cow:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('cow')
        for pattern in rabbit:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('rabbit')
        for pattern in llama:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('llama')
        for pattern in camel:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('camel')
        for pattern in porcupine:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('porcupine')
        for pattern in chicken:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('chicken')
        for pattern in other:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('other')
        for pattern in misclassified:
            if re.findall(pattern, entity):
                table['System_ID'].append(sys_id)
                table['unique_num'].append(uniq_id)
                table['Entity'].append(entity)
                table['Category'].append('misclassified')

    '''Filtering out all entities that were not categorized and labeling as false positives'''
    animal_cats = pd.DataFrame(table)
    check = animal_ents[~animal_ents['unique_num'].isin(animal_cats['unique_num'])]
    check["Category"] = 'false positive'

    '''Concatenating categorized DataFrames and only keeping needed columns'''
    animal_concat = pd.concat([animal_cats, check])
    animal_concat = animal_concat[['System_ID', 'Entity', 'Category']]

    animal_final = animal_ents.merge(animal_concat, on=['System_ID', 'Entity'], how='left')
    animal_final = animal_final[['System_ID', 'Doc', 'Entity', 'Category','Class']]

    return(animal_final)
