import pandas as pd
import plotly.express as px

# dataset avec uniquement les avis commentés (341 avis)
df = pd.read_excel('DATA/reviews_data.xlsx')
print(df.count)

# dataset avec tous les avis (500 avis)
df2 = pd.read_excel('DATA/cleaned_data.xlsx')

# Calcul de la note moyenne des avis de l'échantillon
review_rate_mean = df2['review_rating'].mean().round(2)
print('Note moyenne des avis de l\'échantillon (500 avis):', review_rate_mean)

# Net Promoter Score (NPS) simplifié : % de promoteurs (5 étoiles) - % de détracteurs (1-2 étoiles)
NPS = ((df2['review_rating'] == 5).sum() / len(df2) * 100) - ((df2['review_rating'] <= 2).sum() / len(df2) * 100)
print('Net Promoter Score (NPS) simplifié:', round(NPS, 2)) #24.2 = bon niveau de staisfaction/loyauté.

# Graphique 1 : Répartition des notes
rating_counts = (
    df2['review_rating']
    .dropna()
    .astype(int)
    .value_counts()
    .reindex([1, 2, 3, 4, 5], fill_value=0)
    .rename_axis('note')
    .reset_index(name='nb_avis')
)

fig1 = px.bar(
    rating_counts,
    x='note',
    y='nb_avis',
    title='Répartition des notes (1 à 5)',
    labels={'note': 'Note', 'nb_avis': 'Nombre d\'avis'},
    text='nb_avis'
)
fig1.update_traces(textposition='outside')
fig1.show()

# Graphique 2 : Evolution de la note moyenne
if 'review_datetime_utc' in df2.columns:
    df2['dt'] = pd.to_datetime(df2['review_datetime_utc'], errors='coerce', dayfirst=True)
else:
    df2['dt'] = pd.to_datetime(df2['date'], format='%d/%m/%Y', errors='coerce')

df2['year_month'] = df2['dt'].dt.to_period('M').dt.to_timestamp()

monthly_avg = (
    df2.dropna(subset=['year_month', 'review_rating'])
      .groupby('year_month', as_index=False)['review_rating']
      .mean()
      .rename(columns={'review_rating': 'note_moyenne'})
)

fig2 = px.line(
    monthly_avg,
    x='year_month',
    y='note_moyenne',
    markers=True,
    title='Évolution mensuelle de la note moyenne',
    labels={'year_month': 'Mois', 'note_moyenne': 'Note moyenne'}
)
fig2.update_yaxes(range=[1, 5])
fig2.show()