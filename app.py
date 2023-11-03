from flask import Flask, jsonify, request, redirect, render_template, url_for
from flask_cors import CORS
from threading import Thread
import json
import sys
import os
import requests
import random
from utils import load_confessions, save_confession, get_suggestion, get_feedback, get_password, get_server_name_and_icon

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/tos", methods=["GET"])
def tos():
    return render_template("tos.html")

@app.route("/confessions", methods=["GET"])
def confess():
    new_dic = {}
    data = load_confessions(size=5)

    for a in data:
        check = []
        keys = a.keys()
        for key in keys:
            if key not in check:
                new_dic[key] = a[key]
                check.append(key)
        check.clear()

    new_dic.pop("_id")

    return render_template("confessions.html", data=new_dic)

@app.route("/suggestions/<server_id>", methods=["GET"])
def suggestions(server_id):
    server_id = int(server_id)
    password = request.args.get("password")

    try:
        password_db = get_password(server_id)
    except:
        return render_template("suggestions.html", server_id_error="Server not found, perhaps the bot is not added in the server yet!")

    if password != password_db:
        return render_template("suggestions.html", server_id=server_id, password_error="Incorrect password")

    data = get_suggestion(server_id)

    server_name, server_icon = get_server_name_and_icon(server_id)

    if data:
        data = data[::-1]
        data = data[:20]

    return render_template("suggestions_view.html", data=data, server_name=server_name, server_icon=server_icon)

@app.route("/feedbacks/<server_id>", methods=["GET"])
def feedbacks(server_id):
    server_id = int(server_id)
    password = request.args.get("password")

    try:
        password_db = get_password(server_id)
    except:
        return render_template("feedback.html", server_id_error="Server not found, perhaps the bot is not added in the server yet!")

    if password != password_db:
        return render_template("feedback.html", server_id=server_id, password_error="Incorrect password")


    if password != get_password(server_id):
        return render_template("feedback.html", server_id=server_id, password_error="Incorrect password")

    data = get_feedback(server_id)

    server_name, server_icon = get_server_name_and_icon(server_id)

    if data:
        data = data[::-1]
        data = data[:20]

    return render_template("feedbacks-view.html", data=data, server_name=server_name, server_icon=server_icon)

@app.route("/suggestions", methods=["GET"])
def suggestions_page():
    return render_template("suggestions.html")

@app.route("/feedbacks", methods=["GET"])
def feedback():
    return render_template("feedback.html")

def run():
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=False)


def run_server():
    t = Thread(target=run)
    t.start()


if __name__ == "__main__":
    run()
