import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from datetime import datetime
from keybert import KeyBERT
from afinn import Afinn

df = pd.read_excel('ukraine_raw_dataset.xlsx', usecols='H,D')
all_context = ""
afn = Afinn()

kw_model = KeyBERT()
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

STOP_DATE = np.datetime64("2023-06")
date_str1 = df.iat[0, 0][6] + df.iat[0, 0][7] + df.iat[0, 0][8] + df.iat[0, 0][9] + "-" + df.iat[0, 0][3] + \
            df.iat[0, 0][4]
date_str1 = np.datetime64(date_str1)

for i in range(1,df.shape[0]):
    date_str2 = np.datetime64(date_str1) + np.timedelta64(6, 'M')
    date_str1 = np.datetime64(date_str1)
    new_date_dt = date_str2.astype('datetime64[M]').astype(datetime)

    for j in range(1,df.shape[0]):
        test_date = df.iat[j, 0][6] + df.iat[j, 0][7] + df.iat[j, 0][8] + df.iat[j, 0][9] + "-" + df.iat[j, 0][3] + \
                    df.iat[j, 0][4]
        test_date = np.datetime64(test_date)
        if test_date < new_date_dt:
            all_context = all_context + df.iat[j, 1]
        else:
            continue
    date_str1 = np.datetime64(date_str1) + np.timedelta64(6, 'M')
    if date_str1 > STOP_DATE:
        break
    words = all_context.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    filtered_text = ' '.join(filtered_words)
    keywords = kw_model.extract_keywords(filtered_text, top_n=50)
    scores = [afn.score(keyword[0]) for keyword in keywords]
    sentiment = ['positive' if score > 0 else 'negative' if score < 0 else 'neutral' for score in scores]

    for z in range(len(keywords)):
        keywords[z] = keywords[z] + (sentiment[z],)

    new_df = pd.DataFrame(keywords, columns=['Keyword', 'Score', 'Sentiment'])

    new_df.to_excel(np.datetime_as_string(date_str1)+'.xlsx', index=False)


for i in range(1, df.shape[0]):
    all_context = all_context + df.iat[i, 1]

words = all_context.split()
filtered_words = [word for word in words if word.lower() not in stop_words]
filtered_text = ' '.join(filtered_words)
keywords = kw_model.extract_keywords(filtered_text, top_n=50)
scores = [afn.score(keyword[0]) for keyword in keywords]
sentiment = ['positive' if score > 0 else 'negative' if score < 0 else 'neutral' for score in scores]

for i in range(len(keywords)):
    keywords[i] = keywords[i] + (sentiment[i],)

new_df = pd.DataFrame(keywords, columns=['Keyword', 'Score', 'Sentiment'])

new_df.to_excel('all_context.xlsx', index=False)