import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from wordcloud import WordCloud, STOPWORDS
from datetime import datetime

df = pd.read_excel('ukraine_raw_dataset.xlsx', usecols='H,D')
all_context = ""
stopwords = STOPWORDS
STOP_DATE = np.datetime64("2023-06")
date_str1 = df.iat[0, 0][6] + df.iat[0, 0][7] + df.iat[0, 0][8] + df.iat[0, 0][9] + "-" + df.iat[0, 0][3] + \
            df.iat[0, 0][4]
date_str1 = np.datetime64(date_str1)

for i in range(1, df.shape[0]):
    date_str2 = np.datetime64(date_str1) + np.timedelta64(6, 'M')
    date_str1 = np.datetime64(date_str1)
    new_date_dt = date_str2.astype('datetime64[M]').astype(datetime)

    for j in range(1, df.shape[0]):
        test_date = df.iat[j, 0][6] + df.iat[j, 0][7] + df.iat[j, 0][8] + df.iat[j, 0][9] + "-" + df.iat[j, 0][3] + \
                    df.iat[j, 0][4]
        test_date = np.datetime64(test_date)
        if test_date < new_date_dt:
            all_context = all_context + df.iat[j, 1]
        else:
            continue
    date_str1 = np.datetime64(date_str1) + np.timedelta64(6, 'M')
    wordcloud = WordCloud(width=2000, height=1000, stopwords=stopwords, background_color="white",
                          max_words=500).generate(
        all_context)
    rcParams['figure.figsize'] = 15, 20
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    all_context = ""
    if date_str1 > STOP_DATE:
        break

for i in range(1, df.shape[0]):
    all_context = all_context + df.iat[i, 1]

wordcloud = WordCloud(width=2000, height=1000, stopwords=stopwords, background_color="white", max_words=500).generate(
    all_context)
rcParams['figure.figsize'] = 15, 20
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
