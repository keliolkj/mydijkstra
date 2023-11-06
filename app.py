from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    result = 'Hello, World!'
    return f"<pre>{result}</pre>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=90)
