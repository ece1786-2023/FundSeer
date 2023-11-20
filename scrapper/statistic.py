import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def getTopKWords(df, kwords):

    stop = set(stopwords.words('english'))
    counter = Counter()

    descriptions = df['Description'].values

    for d in descriptions:
            counter.update([word.lower()
                            for word
                            in re.findall(r'\w+', d)
                            if word.lower() not in stop and len(word) > 2])
    topk = counter.most_common(kwords)
    return topk


# setting default parameters of WordCloud object
wordcloud_args = dict(
    width = 800,
    height = 800,
    background_color ='white',
    min_font_size = 10
    )

# fucntion to plot word cloud
def plotWordCloud(dictionary, **kwargs):
    wordcloud = WordCloud(**kwargs)

    wordcloud.generate_from_frequencies(dict(dictionary))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

file_path = 'scrapper/data/campaign_info_100001_200000.csv'

df = pd.read_csv(file_path)

# Add a new column 'Goal Met' with 1 if raised amount > goal amount, else 0
df['Goal Met'] = (df['Raised Amount'] > df['Goal Amount']).astype(int)

statistics = df.describe()

head = df.head()

# Print the results
print("\nBasic Statistics:")
print(statistics)

print("\nFirst Few Rows:")
print(head)

success = df[df['Goal Met'] == 1]
fail = df[df['Goal Met'] == 0]
topk_success = getTopKWords(success, 50)
plotWordCloud(topk_success, **wordcloud_args)
topk_fail = getTopKWords(fail, 50)
plotWordCloud(topk_fail, **wordcloud_args)

# Plot histogram of description lengths for both successful and unsuccessful campaigns
plt.figure(figsize=(12, 6))
plt.hist([success['Description'].apply(len), fail['Description'].apply(len)],
         bins=20, alpha=0.7, color=['green', 'red'], label=['Success', 'Fail'])
plt.title('Histogram of Description Lengths for Successful and Unsuccessful Campaigns')
plt.xlabel('Description Length')
plt.ylabel('Frequency')
plt.legend()
plt.show()
