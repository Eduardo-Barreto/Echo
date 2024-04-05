from flask import Flask, render_template, Response, request
from flask_cors import CORS

import json
import logging
from tinydb import TinyDB, Query
from datetime import datetime

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

db = TinyDB("logs.json")
app = Flask(__name__)
CORS(app)


@app.route("/ping")
def ping():
    ip_address = request.remote_addr

    log_entry = {
        "timestamp": str(datetime.now()),
        "ip_address": ip_address,
        "action": "ping",
        "parameters": {},
    }
    logger.info(log_entry)

    db.insert(log_entry)
    return {"response": "pong"}


@app.route("/echo", methods=["POST"])
def echo():
    data = request.json

    ip_address = request.remote_addr

    log_entry = {
        "timestamp": str(datetime.now()),
        "ip_address": ip_address,
        "action": "connect",
        "parameters": data,
    }
    logger.info(log_entry)

    db.insert(log_entry)

    return data


@app.route("/dash")
def dash():
    return render_template("dashboard.html")


@app.route("/info")
def list_logs():
    logs = db.all()
    logs_with_ids = [{"doc_id": log.doc_id, "data": log} for log in logs]
    return render_template("log.html", logs=logs_with_ids)


@app.route("/logs/<id>", methods=["DELETE"])
def delete_log(id: int):
    db.remove(doc_ids=[int(id)])

    resp = Response()
    resp.headers["HX-Redirect"] = "/dash"
    return resp


@app.route("/logs/all", methods=["DELETE"])
def clear_all_logs():
    db.truncate()

    resp = Response()
    resp.headers["HX-Redirect"] = "/dash"
    return resp
