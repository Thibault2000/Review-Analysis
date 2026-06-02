### Librairies ###
import pandas as pd

# Chargement du fichier Excel
df = pd.read_excel('DATA/data.xlsx')
print(df.head())
print(df.columns)

### Nettoyage des données ###
print(df["review_datetime_utc"].dtype)
df['date'] = pd.to_datetime(df['review_datetime_utc'], dayfirst=True, errors='coerce')

cols = ['rating','review_text','review_rating','date']

cleaned_df = df[cols]

# Sauvegarde du DataFrame nettoyé dans un nouveau fichier Excel (tous les derniers 500 avis)
cleaned_df.to_excel('DATA/cleaned_data.xlsx', index=False)

reviews_df = cleaned_df[cleaned_df['review_text'].notna() & cleaned_df['review_text'].astype(str).str.strip().ne('')]
reviews_df.dropna()

# Sauvegarde du DataFrame des avis nettoyés dans un nouveau fichier Excel
reviews_df.to_excel('DATA/reviews_data.xlsx', index=False)
