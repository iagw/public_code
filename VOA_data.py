
import os
import numpy as np
import pandas as pd
home_folder = os.getenv('HOME')
folderpath = f'{home_folder}/BHA-hydro-project-2022-GIS-folder/uk-englandwales-ndr-2017-listentries-compiled-epoch-0031-baseline-csv/'
os.chdir(folderpath)

file1 = open('uk-englandwales-ndr-2017-listentries-compiled-epoch-0031-baseline-csv.csv',
             'r',
             encoding='latin1')
dfLines = pd.DataFrame(file1.readlines(), columns=['value'])
dfLines['starcount'] = dfLines['value'].map(lambda y: y.count('*'))
dfLinesindex = dfLines[dfLines['starcount'] == 3].index.to_list()

# iter_len = len(dfLinesindex)
for x in dfLinesindex:
    # if x == dfLinesindex[1]:
    templine = dfLines.iloc[x]['value'].replace('\n', '') + dfLines.loc[x+1]['value']
    # print(templine)
    # print(templine.count('*'))
    # print(dfLines.iloc[x]['value'].replace('\n', ''))
    # print(dfLines.iloc[x+1]['value'].replace('\n', ''))
    dfLines.loc[x, 'value'] = templine

for x in dfLinesindex:
    dfLines = dfLines.drop(x+1)

dfLines['starcount2'] = dfLines['value'].map(lambda y: y.count('*'))
dfLines = dfLines.reset_index(drop=True)

df = dfLines['value'].str.split('*', expand=True)
df = df.iloc[:, :-1]

collist = ['Incrementing Entry Number',
           'Billing Authority Code',
           'NDR Community Code ',
           'BA Reference Number',
           'Primary And Secondary Description Code',
           'Primary Description Text',
           'Unique Address Reference Number UARN',
           'Full Property Identifier',
           'Firms Name',
           'Number Or Name',
           'Street ',
           'Town ',
           'Postal District ',
           'County ',
           'Postcode ',
           'Effective Date ',
           'Composite Indicator ',
           'Rateable Value ',
           'Appeal Settlement Code ',
           'Assessment Reference ',
           'List Alteration Date ',
           'SCAT Code And Suffix ',
           'Sub Street level 3 ',
           'Sub Street level 2 ',
           'Sub Street level 1 ',
           'Case Number ',
           'Current From Date ',
           'Current To Date '
           ]

collist = [x.strip().replace(' ', '_').lower() for x in collist]
df.columns = collist

# df.to_csv('parsed_uk-englandwales-ndr-2017-listentries-compiled-epoch-0031-baseline-csv.csv.gzip',
#           encoding='Utf-8',
#           compression='gzip',
#           index=None)
#
# df.to_parquet('parsed_uk-englandwales-ndr-2017-listentries-compiled-epoch-0031-baseline-csv.gzip.parquet',
#           compression='gzip',
#           index=None)

# dfhydro = df[df['scat_code_and_suffix'] == '746U']
# dfhydro2 = df[df['primary_description_text'].str.contains('POWER')]
dfhydro3 = df[df['primary_description_text'].isin(['HYDRO POWER STATION AND PREMSIES', 'HYDRO POWER STATION AND PREMISES'])]

dfhydro3.to_csv('hydro_valuations.csv',
               encoding='Utf-8',
               index=None)