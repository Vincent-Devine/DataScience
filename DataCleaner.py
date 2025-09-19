import pandas
dtype={"user_id": int, "username": "string"}
df = pandas.read_csv("RawData/age_genre.csv")
df = df.drop(columns=['INSEE', 'NOM', 'EPCI', 'REG'])
df['DEP'] = df['DEP'].map(lambda x: x.lstrip('D'))
df = df.groupby(['DEP']).sum()
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df.insert(10, 'F', df.iloc[:, 1:10].sum(axis=1))
df['H'] = df.iloc[:, 12:].sum(axis=1)
df['0-2'] = df['H0-2'] + df['F0-2']
df['3-5'] = df['H3-5'] + df['F3-5']
df['6-10'] = df['H6-10'] + df['F6-10']
df['11-17'] = df['H11-17'] + df['F11-17']
df['18-24'] = df['H18-24'] + df['F18-24']
df['25-39'] = df['H25-39'] + df['F25-39']
df['40-54'] = df['H40-54'] + df['F40-54']
df['55-64'] = df['H55-64'] + df['F55-64']
df['65-79'] = df['H65-79'] + df['F65-79']
df['80+'] = df['H80+'] + df['F80+']
df['TOT'] = df['H'] + df['F']
df.to_csv("Data/age_genre.csv")