
# Machine Learning Projects

## 1. SMS Spam Detector
Live Demo: https://spam-detector-yc5s.onrender.com
Tech Stack: Python, Flask, Scikit-learn, TF-IDF, MultinomialNB  

An SMS classification project that detects Spam vs Ham messages.

## Project Structure
- `spam-detector/`: Flask app with ML model deployed on Render
- `train_model.py`: Script to train the model
- `requirements.txt`: Dependencies

## Features
- Detects if an SMS is Spam or Ham
- Simple UI with result highlighting

## How it Works
1. Uses TF-IDF vectorization
2. Multinomial Naive Bayes classification
3. Deployed on Render with Flask
