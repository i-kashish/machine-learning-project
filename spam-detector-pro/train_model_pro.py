import pandas as pd
import pickle
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

nltk.download('stopwords')
from nltk.corpus import stopwords

# Dataset: Use SMS Spam Collection Dataset
url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
df = pd.read_csv(url, sep='\t', names=['label', 'message'])

# Preprocessing
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words=stopwords.words('english'), max_features=5000)
X = tfidf.fit_transform(df['message']).toarray()
y = df['label']

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model: Logistic Regression - better than Naive Bayes
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Test Accuracy
pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, pred) * 100:.2f}%")

# Save model and vectorizer
pickle.dump(model, open('spam_model_pro.pkl', 'wb'))
pickle.dump(tfidf, open('vectorizer_pro.pkl', 'wb'))
print("Model and Vectorizer saved!")
