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
    data = load_confessions()

    keys = random.sample(list(data.keys()), 5)
    new_dic = {}
    for key in keys:
        new_dic[key] = data[key]

    print(new_dic)
    return render_template("index.html", data=new_dic)


def run():
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)


def run_server():
    t = Thread(target=run)
    t.start()


if __name__ == "__main__":
    run()
