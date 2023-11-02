from flask import Flask, jsonify, request, redirect, render_template
from flask_cors import CORS
from threading import Thread
import json
import sys
import os
import requests
import random
from utils import load_confessions, save_confession

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
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

    return render_template("index.html", data=new_dic)


def run():
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=False)


def run_server():
    t = Thread(target=run)
    t.start()


if __name__ == "__main__":
    run()
