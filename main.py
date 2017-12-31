from flask import Flask, config, render_template, request
import redis
import re

app = Flask(__name__)
red = redis.StrictRedis(host='localhost', port=6379, db=0)
app.config.from_object('config')


def match_string(string):
    return re.match(r"^HappyNewYearOurDearStudentsWeLoveYou.*", string)


@app.route('/new', methods=["POST", "GET"])
def new():
    if request.method == "POST":
        text = request.values.get("text")
        if not text:
            return "Ну напиши что-нибудь уже!"
        if match_string(text):
            return app.config["FLAG"]
        red.lpush('new_year', text)
        return "Спасибо за поздравление. Теперь оно доступно на страничке /list"
    return render_template('new.html')


@app.route('/list')
def list_all():
    data = [x.decode() for x in red.lrange("new_year", 0, -1)]
    return render_template("list.html", items=data)


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.run(debug=True)
