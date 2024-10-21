from flask import Flask, Blueprint

app = Flask(__name__)

if __name__ == "__main__":
    app.run("0.0.0.0", 3750)

