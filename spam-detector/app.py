from flask import Flask, render_template_string, request
import pickle

app = Flask(__name__)
model = pickle.load(open('spam_model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>SMS Spam Detector</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        textarea { width: 100%; height: 100px; padding: 10px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
     .result { margin-top: 20px; padding: 15px; font-size: 20px; }
     .spam { background: #ffdddd; color: red; }
     .ham { background: #ddffdd; color: green; }
    </style>
</head>
<body>
    <h2>SMS Spam Detector</h2>
    <form method="post">
        <textarea name="message" placeholder="Type SMS here">{{ message }}</textarea><br><br>
        <button type="submit">Check</button>
    </form>
    {% if result %}
        <div class="result {{ result }}">
            Result: {{ result.upper() }}
        </div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    message = ""
    if request.method == 'POST':
        message = request.form['message']
        msg_transformed = vectorizer.transform([message])
        result = model.predict(msg_transformed)[0]
    return render_template_string(HTML, result=result, message=message)

if __name__ == '__main__':
    app.run()
