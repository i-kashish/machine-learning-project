from flask import Flask, render_template_string, request
import pickle
import numpy as np

app = Flask(__name__)

# Load model and vectorizer
model = pickle.load(open('spam_model_pro.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer_pro.pkl', 'rb'))

# Get feature names for highlighting words
feature_names = vectorizer.get_feature_names_out()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>SMS Spam Detector Pro</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --text: #e2e8f0;
            --accent: #38bdf8;
            --spam: #ef4444;
            --ham: #22c55e;
        }
        body {
            background: var(--bg);
            color: var(--text);
            font-family: system-ui, sans-serif;
            display: flex;
            justify-content: center;
            padding: 20px;
            margin: 0;
        }
       .container {
            width: 100%;
            max-width: 700px;
        }
       .card {
            background: var(--card);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: var(--accent);
            margin-top: 0;
        }
        textarea {
            width: 100%;
            height: 120px;
            background: var(--bg);
            border: 1px solid #334155;
            color: var(--text);
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
            box-sizing: border-box;
            resize: vertical;
        }
        button {
            width: 100%;
            padding: 12px;
            background: var(--accent);
            border: none;
            border-radius: 8px;
            color: var(--bg);
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 12px;
        }
       .result {
            margin-top: 20px;
            padding: 16px;
            border-radius: 8px;
            text-align: center;
        }
       .spam { background: rgba(239, 68, 68, 0.2); border: 1px solid var(--spam); }
       .ham { background: rgba(34, 197, 94, 0.2); border: 1px solid var(--ham); }
       .result h2 { margin: 0 0 8px 0; }
       .confidence {
            background: var(--bg);
            border-radius: 20px;
            height: 10px;
            margin-top: 8px;
        }
       .confidence-bar {
            height: 100%;
            border-radius: 20px;
            transition: width 0.5s;
        }
       .keywords { font-size: 14px; margin-top: 12px; opacity: 0.8; }
       .keywords span {
            background: var(--bg);
            padding: 4px 8px;
            border-radius: 4px;
            margin: 2px;
            display: inline-block;
        }
       .history { margin-top: 24px; }
       .history-item {
            font-size: 14px;
            opacity: 0.7;
            padding: 8px 0;
            border-bottom: 1px solid #334155;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>SMS Spam Detector Pro</h1>
            <form method="POST">
                <textarea name="message" placeholder="Paste SMS here..." required>{{ message }}</textarea>
                <button type="submit">Analyze SMS</button>
            </form>

            {% if prediction %}
            <div class="result {{ 'spam' if prediction == 'SPAM' else 'ham' }}">
                <h2>{{ prediction }}</h2>
                <p>Confidence: {{ confidence }}%</p>
                <div class="confidence">
                    <div class="confidence-bar" style="width: {{ confidence }}%; background: {{ '#ef4444' if prediction == 'SPAM' else '#22c55e' }};"></div>
                </div>
                {% if top_words %}
                <div class="keywords">
                    Top spam indicators:
                    {% for word in top_words %}
                    <span>{{ word }}</span>
                    {% endfor %}
                </div>
                {% endif %}
            </div>
            {% endif %}
            <p style="text-align:center; margin-top:20px; opacity:0.5; font-size:12px;"> Built by Tera Naam 🚀 </p>
        </div>
    </div>
</body>
</html>
'''

def get_top_words(message, proba):
    if proba < 0.5: # If Ham, don't show spam words
        return []
    vec = vectorizer.transform([message]).toarray()[0]
    # Get indices of words present in message
    indices = np.where(vec > 0)[0]
    # Get coefficients from model
    coefs = model.coef_[0]
    # Get top spam words
    word_scores = [(feature_names[i], coefs[i] * vec[i]) for i in indices]
    word_scores.sort(key=lambda x: x[1], reverse=True)
    return [word for word, score in word_scores[:5] if score > 0]

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = 0
    message = ""
    top_words = []

    if request.method == 'POST':
        message = request.form['message']
        data = vectorizer.transform([message]).toarray()
        proba = model.predict_proba(data)[0]
        pred_class = model.predict(data)[0]

        prediction = "SPAM" if pred_class == 1 else "HAM"
        confidence = round(max(proba) * 100, 1)
        top_words = get_top_words(message, proba[1])

    return render_template_string(HTML_TEMPLATE,
                                  prediction=prediction,
                                  confidence=confidence,
                                  message=message,
                                  top_words=top_words)

if __name__ == '__main__':
    app.run(debug=True)
