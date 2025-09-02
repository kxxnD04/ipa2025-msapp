from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
import os
from bson.objectid import ObjectId

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")
client = MongoClient(mongo_uri)
db = client[db_name]
routers_col = db["routers"]
status_col = db["router_status"]  # collection ของ interface status

app = Flask(__name__)


# หน้า list routers
@app.route("/")
def main():
    routers = list(routers_col.find())
    return render_template("index.html", routers=routers)


# เพิ่ม router
@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")
    if ip and username and password:
        routers_col.insert_one({"ip": ip, "username": username, "password": password})
    return redirect(url_for("main"))


# ลบ router
@app.route("/delete", methods=["POST"])
def delete_router():
    router_id = request.form.get("id")
    if router_id:
        try:
            routers_col.delete_one({"_id": ObjectId(router_id)})
        except Exception:
            pass
    return redirect(url_for("main"))


# หน้าแสดง interface status ของ router
@app.route("/router/<router_ip>")
@app.route("/router/<router_ip>")
def router_detail(router_ip):
    # ดึงข้อมูลล่าสุด 5 documents ของ router จาก collection router_status
    # Sort by timestamp in descending order and limit to 3
    status_data = list(
        status_col.find({"router_ip": router_ip}).sort("timestamp", -1).limit(5)
    )

    # Pass the entire list of documents to the template
    return render_template(
        "router_detail.html", router_ip=router_ip, status_data=status_data
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
