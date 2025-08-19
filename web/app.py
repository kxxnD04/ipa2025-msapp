from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
import os

mongo_uri  = os.environ.get("MONGO_URI")
db_name    = os.environ.get("DB_NAME")
# client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient("mongodb://mongo:27017/")
client = MongoClient(mongo_uri)

# mydb = client["mydatabase"]
mydb = client["ipa2025"]
# mycol = mydb["mycollection"]
mycol = mydb["routers"]

sample = Flask(__name__)

@sample.route("/")
def main():
    routers = list(mycol.find())
    return render_template("index.html", routers=routers)

@sample.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        mycol.insert_one({
            "ip": ip,
            "username": username,
            "password": password
        })
    return redirect(url_for("main"))

@sample.route("/delete", methods=["POST"])
def delete_router():
    router_id = request.form.get("id")
    if router_id:
        from bson.objectid import ObjectId
        try:
            mycol.delete_one({"_id": ObjectId(router_id)})
        except Exception:
            pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)
