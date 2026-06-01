from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

html_form = '''
<!DOCTYPE html>
<html>
<head>
    <title>Student Score Analyzer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #1e3c72, #2a5298);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }

        .container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            width: 400px;
            box-shadow: 0px 8px 25px rgba(0,0,0,0.3);
            text-align: center;
        }

        h1 {
            color: #1e3c72;
            margin-bottom: 25px;
        }

        input {
            width: 90%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
        }

        button {
            background: #1e3c72;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: 0.3s;
        }

        button:hover {
            background: #2a5298;
            transform: scale(1.05);
        }

        .result {
            margin-top: 20px;
            padding: 15px;
            background: #f4f7ff;
            border-radius: 10px;
            font-size: 18px;
            color: #222;
            font-weight: bold;
        }

        .footer {
            margin-top: 20px;
            font-size: 13px;
            color: gray;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>🎓 Student Score Analyzer</h1>

    <form method="post">
        <input type="text" name="name" placeholder="Enter Student Name" required>

        <input type="number" name="marks" placeholder="Enter Marks (0-100)" min="0" max="100" required>

        <br><br>

        <button type="submit">Analyze Score</button>
    </form>

    {% if result %}
        <div class="result">
            {{ result }}
        </div>
    {% endif %}

    <div class="footer">
        Docker Compose Microservices Project
    </div>
</div>

</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        try:
            name = request.form['name']
            marks = int(request.form['marks'])

            resp = requests.post(
                'http://backend:5000/calculate',
                json={'name': name, 'marks': marks}
            )

            data = resp.json()

            result = f"{name} got {data['percentage']}% Grade: {data['grade']}"

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template_string(html_form, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
