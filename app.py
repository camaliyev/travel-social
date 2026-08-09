from flask import Flask

print("App is starting...")

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

if __name__ == "__main__":
    print("Running Flask...")
    app.run(debug=True)