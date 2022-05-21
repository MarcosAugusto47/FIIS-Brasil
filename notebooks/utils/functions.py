def convert_string_to_float(df, colnames):
    for colname in colnames:
        df[colname] = df[colname].str.replace('R$', "", regex=False)
        df[colname] = df[colname].str.replace('.', "", regex=False)
        df[colname] = df[colname].str.replace(',', ".", regex=False)
        df[colname] = df[colname].apply(lambda x: float(x))
    return df