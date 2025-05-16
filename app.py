from flask import Flask , jsonify , render_template
from Review_Automation import  Start_Project_Review


app = Flask(__name__,template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-review",methods=['GET'])
def Run_Review():
    return jsonify({"Status":Start_Project_Review()})


if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5000)
