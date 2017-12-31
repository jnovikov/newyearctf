from flask import Flask, config

app = Flask(__name__)


@app.route('/')
def hello_world():
    return


if __name__ == '__main__':
    app.run()
