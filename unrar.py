#!/usr/bin/env python3

from flask import Flask, request, render_template, send_file
import os
import fnmatch
from subprocess import check_output, CalledProcessError

from config import FILES_PATH

app = Flask(__name__)

if not FILES_PATH[-1] == os.sep:
    FILES_PATH = FILES_PATH + os.sep

rars = []
for root, dirnames, filenames in os.walk(FILES_PATH):
    for fn in fnmatch.filter(filenames, "*.rar"):
        rars.append((root, fn))

@app.route('/unrar', methods=["POST"])
def unrar():
    if request.form.get("id", None) and request.form["id"].isdigit():
        path, fn = rars[int(request.form["id"])]
        try:
            rar_outp = check_output(["unrar", "x", path + os.sep + fn, "-o-"], cwd=path)
        except Exception as e:
            rar_outp = e.output
        return render_template("unrar.html", outp=rar_outp.decode('utf-8').strip())
    else:
        return render_template("unrar.html", error="Invalid selection")

@app.route('/')
def index():
    return render_template('index.html', rars=enumerate(rars))

if __name__ == "__main__":
    app.run(port=23473, debug=True)
