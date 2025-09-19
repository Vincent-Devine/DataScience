import pandas

# age and gender
def CleanAgeGender():
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


# job type
def CleanJobType():
    df = pandas.read_csv("RawData/categorie_socio-profesionnelle.csv",sep=';')
    df = df.drop(columns=['Code Officiel R\u00E9gion', 'Nom Officiel D\u00E9partement', 'Code interne de la variable', 'Nom Officiel R\u00E9gion', "Ann\u00E9e de r\u00E9f\u00E9rence g\u00E9ographique"])
    df = df.rename(columns={"Code Officiel D\u00E9partement": "DEP", "Valeur": "VAL", "Ann\u00E9e": "ANNEE", "Nom de la variable": "CAT"})
    df = df[df['ANNEE'] == 2019]
    df = df.drop(columns=['ANNEE'])
    df.loc[df['CAT'] == 'Professions interm\u00E9diaires Actifs ayant un emploi', 'CAT'] = 'intermediaire actif'
    df.loc[df['CAT'] == 'Professions interm\u00E9diaires Ch\u00F4meurs', 'CAT'] = 'intermediaire chomeur'
    df.loc[df['CAT'] == 'Employ\u00E9s Actifs ayant un emploi', 'CAT'] = 'employe actif'
    df.loc[df['CAT'] == 'Employ\u00E9s Ch\u00F4meurs', 'CAT'] = 'employe chomeur'
    df.loc[df['CAT'] == 'Cadres et professions intellectuelles sup\u00E9rieures Actifs ayant un emploi', 'CAT'] = 'cadre sup actif'
    df.loc[df['CAT'] == 'Cadres et professions intellectuelles sup\u00E9rieures Ch\u00F4meurs', 'CAT'] = 'cadre sup chomeur'
    df.loc[df['CAT'] == 'Agriculteurs Actifs ayant un emploi', 'CAT'] = 'agriculteur actif'
    df.loc[df['CAT'] == 'Agriculteurs Ch\u00F4meurs', 'CAT'] = 'agriculteur chomeur'
    df.loc[df['CAT'] == 'Ouvriers Actifs ayant un emploi', 'CAT'] = 'ouvrier actif'
    df.loc[df['CAT'] == 'Ouvriers Ch\u00F4meurs', 'CAT'] = 'ouvrier chomeur'
    df.loc[df['CAT'] == 'Artisans, commer\u00E7ants, chefs d\'entreprise Ch\u00F4meurs', 'CAT'] = 'artisant / commercant / chef d\'entreprise chomeur'
    df.loc[df['CAT'] == 'Artisans, commer\u00E7ants, chefs d\'entreprise Actifs ayant un emploi', 'CAT'] = 'artisant / commercant / chef d\'entreprise actif'
    df = df.sort_values(by=['DEP'])
    df = df.reset_index(drop=True)
    df.to_csv("Data/categorie_socio-profesionnelle.csv", index=False)

