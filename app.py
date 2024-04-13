from flask import Flask,render_template,request
from dataset import generate_dataset
from training import train_classifier
from detection import detector
from attendance import daa

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/registration", methods = ['POST',"GET"])
def registration():
    output = request.form.to_dict()
    roll = output["roll"]
    generate_dataset(roll)
    name = output["name"]
    daa(name,roll)
    return render_template("index.html", name=name)

@app.route("/result", methods = ['POST',"GET"])
def result():
    train_classifier("data")
    na=detector()
    return render_template("index.html", name=na)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
