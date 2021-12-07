"""
Categorizing the assay entities from the custom NER model.
"""
import numpy as np
import pandas as pd
import re

def clean_ents(df):
    """
    Filtering entity output doc to only include assay entities and categorizing entities.

    Input: df (dataframe) - uncategorized entities
    Returns: assay_final (dataframe) - categorized entities
    """
    assay_ents = df[df.Class=='assay']
    assay_ents['unique_num'] = assay_ents.reset_index().index

    table2 = {'System_ID':[], 'unique_num': [], 'Entity':[], 'Category':[]}

    '''Regex rules for categorization'''

    flow = [r'^(?!\D*(?:[Ll]ateral( - )?))[Ff]low [Cc]ytomet(ry)?|[Ff]low-[Cc]ytometry|[Ff]low [Cc]ytometry|Flowcytometric|[Ff]low [Cc]ytometer|[Ff]low [Cc]ytometric|flowcytometry']
    ELISA = [r'ELISA|enzyme-linked immunosorbent assay(s)?|enzyme linked immunosorbent assay(s)?|EUROIMMUN|EIA(s)?|EDI(s)?']
    neutralization = [r'^(?!\D*(?:PRNT(50)? |[Pp]laque [Rr]eduction ))[Nn]eutrali[zs]ation(s)?|(?<!in vitro )[Mm]icroneutrali[zs]ation|nAb RVPN assay|nAb assays']
    immunoassay = [r'^(?!\D*(?:([Ll]ateral( -)?)?[Ff]low|[Cc]hemiluminescence ))[Ii]mmunoassay(s)?|[Mm]ultiplex (immuno)?[Aa]ssay(s)?|(?<![Cc]hemiluminescence )[Ee]nzyme [Ii]mmunoassay(s)?|microsphere-based immunoassay|Luminex-based microsphere immunoassay']
    lateral_flow = ['[Ll]ateral [Ff]low|[Ll]ateral-[Ff]low|[Ff]low [Ii]mmunoassay|immunochromatographic assay']
    serology = [r'[Ss]erology|(?<![Cc]hemiluminescent )[Ss]erological(?! [Cc]hemiluminescence)|[Ss]erologic(al)? assays']
    PRNT = [r'PRNT|PRNT50|(?<![Cc]hemiluminescence )[Rr]eduction [Nn]eutrali[sz]ation|[Pp]laque [Rr]eduction [Nn]eutrali[sz]ation|[Pp]laque [Rr]eduction( [Nn]eutrali[sz]ing)?|reduction assay']
    pseudotype = [r'[Ll]entiviral|[Pp]seudotype(d)?']
    ELISpot = [r'enzyme-linked immunospot|[Ee][Ll][Ii][Ss][Pp][Oo][Tt]|enzyme-linked immunosorbent spot|enzyme-linked immunosorbent spot']
    chemiluminescence= [r'[Cc]hemiluminescence|[Cc]hemiluminescent']
    pseudovirus = [r'[Pp]seudovirus [Aa]ssay(s)?|[Pp]seudovirus|pseudovirus neutrali[zs]ation assay(s)?|pseudovirion neutralization assay']
    immunofluorescence = [r'[Ii]mmunofluorescence']
    in_vitro = [r'[Ii]n vitro|Vitros assay']
    luciferase = [r'[Ll]uciferase']
    other = ['(?<![Ss]erological )[Ww]estern [Bb]lot(s)?|LFRET|IgG assay|microarray assay|High sensitivity assays|in silico immunization assays|in vivo assays|IgG avidity assay|Diasorin assay|Molecular assays|multicolor FluoroSpot assay|inhibition assay|immunity assays|Antibody assays|PK assay|competition assay|laboratory cell infection assay|parallel diagnostic assay|plaque assay|Western immunoblot tests|qSAT assays|quantitative assay|bead-based assay|Luminex-bead based assay|Plaque assay|sVNT assay|MN assay(s)?|secretion assays|SPR assay|multiplex bead assay|microwell assay|Microsphere-Based Inhibition Assay|life virus assay|vaccine protection assay|bAb assay|interferon-γ-based assays|inhibitory assay|IFA assays|ADE assay|[Mm]icrosphere-[Bb]ased [Aa]ntibody [Aa]ssay|microwell assay|SPR assays|bimolecular fluorescence complementation assay|cytopathic assays|microarray-based assays|live SARS-CoV-2 infection assay|live SARS-CoV-2 virus assay|microsphere-based( antibody)? assay|cell-free assay|qSAT assays|multicolor FluoroSpot Assay']
    misclassified = [r'gamma interferon \(IFN-γ\)|camel/human|interferon γ-producing CD4+|in silico sorting CD4+ T-cells|(?<!flow cytometryTotal )[Ll]ymphocyte|virus-like particle (VLP) vaccine']
    falsePos = [r'LDH|lactate dehydrogenase|interferon-gamma(?! ELISpot)|interferon gamma']

    for index, row in assay_ents.iterrows():
        sys_id = assay_ents.loc[index, 'System_ID']
        entity = assay_ents.loc[index, 'Entity']
        animal = assay_ents.loc[index, 'Class']
        uniq_id = assay_ents.loc[index, 'unique_num']
        for pattern in flow:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('flow cytometry')
        for pattern in ELISA:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('ELISA')
        for pattern in neutralization:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('neutralization assays')
        for pattern in immunoassay:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('immunoassays')
        for pattern in lateral_flow:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('lateral flow assays')
        for pattern in serology:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('serological assays')
        for pattern in PRNT:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('PRNT')
        for pattern in pseudotype:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('lentiviral pseudotype assays')
        for pattern in ELISpot:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('ELISpot')
        for pattern in chemiluminescence:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('chemiluminescent assays')
        for pattern in pseudovirus:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('pseudovirus assays')
        for pattern in immunofluorescence:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('immunofluorescence assays')
        for pattern in in_vitro:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('in vitro assays')
        for pattern in luciferase:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('luciferase assays')
        for pattern in other:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('other assays')
        for pattern in misclassified:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('misclassified')
        for pattern in falsePos:
            if re.findall(pattern, entity):
                table2['System_ID'].append(sys_id)
                table2['unique_num'].append(uniq_id)
                table2['Entity'].append(entity)
                table2['Category'].append('false positive')

    assay_cats = pd.DataFrame(table2)
    check2 = assay_ents[~assay_ents['unique_num'].isin(assay_cats['unique_num'])]

    '''
    Doing another round of regex categorization on currently un-categorized data due to severe overlap with neutralization and binding assays
    '''
    table3 = {'System_ID':[], 'unique_num': [], 'Entity':[], 'Category':[]}
    neutralization = [r'[Nn]eutrali[sz]ation|[Nn]eutrali[sz]ing']
    binding = [r'[Bb]inding']

    for index, row in check2.iterrows():
        sys_id = check2.loc[index, 'System_ID']
        entity = check2.loc[index, 'Entity']
        animal = check2.loc[index, 'Class']
        uniq_id = check2.loc[index, 'unique_num']
        for pattern in neutralization:
            if re.findall(pattern, entity):
                table3['System_ID'].append(sys_id)
                table3['unique_num'].append(uniq_id)
                table3['Entity'].append(entity)
                table3['Category'].append('neutralization assays')
        for pattern in binding:
            if re.findall(pattern, entity):
                table3['System_ID'].append(sys_id)
                table3['unique_num'].append(uniq_id)
                table3['Entity'].append(entity)
                table3['Category'].append('binding assays')

    '''Filtering out all entities that were not categorized and labeling as false positives'''
    assay_more = pd.DataFrame(table3)
    check3 = check2[~check2['unique_num'].isin(assay_more['unique_num'])]
    check3["Category"] = 'false positive'

    '''Concatenating categorized DataFrames and only keeping needed columns'''
    assay_concat = pd.concat([assay_cats, assay_more, check3])
    assay_concat = assay_concat[['System_ID', 'Entity', 'Category']]

    assay_final = assay_ents.merge(assay_concat, on=['System_ID', 'Entity'], how='left')
    assay_final = assay_final[['System_ID', 'Doc', 'Entity', 'Category','Class']]

    return(assay_final)
