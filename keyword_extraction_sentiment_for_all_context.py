import pandas as pd
import nltk
from nltk.corpus import stopwords
from afinn import Afinn

df = pd.read_excel('ukraine_raw_dataset.xlsx', usecols='H,D')
all_context = ""
afn = Afinn()

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

for i in range(1, df.shape[0]):
    all_context = all_context + df.iat[i, 1]

words = all_context.split()
filtered_words = [word for word in words if word.lower() not in stop_words]
scores = [afn.score(keyword) for keyword in filtered_words]
sentiment = ['positive' if score > 0 else 'negative' if score < 0 else 'neutral' for score in scores]

data = list(zip(filtered_words,sentiment))

new_df = pd.DataFrame(data, columns=['Keyword', 'Sentiment'])

new_df.to_excel('all_words.xlsx', index=False)