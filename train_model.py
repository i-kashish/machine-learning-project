import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
df = pd.read_csv(url, sep='\t', names=['label', 'message'])

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['message'])

model = MultinomialNB()
model.fit(X, df['label'])

pickle.dump(model, open('spam_model.pkl', 'wb'))
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))
print("Done! Both files created: spam_model.pkl and vectorizer.pkl")