import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import plotly.express as px

df = pd.read_excel('DATA/reviews_data.xlsx')

avis_negatifs = df[df['review_rating'] <= 3]['review_text'].dropna()

mots_vides = [
    "le", "la", "les", "de", "des", "un", "une", "et", "est", "en", "que", "qui", 
    "pour", "dans", "sur", "pas", "ne", "ce", "il", "y", "a", "au", "aux", "avec", "tout", "mon", "ma", "mes", "c'est", "nous", "vous", "je", "j'ai", "qu'il", "leroy", "merlin", "leroymerlin", "on", "me", "du", "qu", "ils", "ont", "suis","aujourd'hui", "aujourd", "hui", "nice"
]

# ngram_range=(2, 3) -> On veut les expressions de 2 ou 3 mots.
vectorizer = CountVectorizer(ngram_range=(2, 3), stop_words=mots_vides)
X = vectorizer.fit_transform(avis_negatifs)

frequences = X.sum(axis=0).A1
mots_cles = vectorizer.get_feature_names_out()

df_frictions = pd.DataFrame({
    'Friction': mots_cles,
    'Frequence': frequences
}).sort_values(by='Frequence', ascending=False).head(10)

print(df_frictions)

df_frictions = df_frictions.sort_values(by='Frequence', ascending=True)

fig = px.bar(
    df_frictions, 
    x='Frequence', 
    y='Friction', 
    orientation='h', 
    title='Top 10 des Frictions Majeures (Avis ≤ 3 étoiles)',
    color_discrete_sequence=['#ef553b'] # Un rouge qui alerte
)

fig.show()