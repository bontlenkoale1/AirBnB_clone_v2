#!/usr/bin/python3
""" Starts a Flash Web Application
Your Web Application must be listening on 0.0.0.0, port 5000
"""
from flask import Flask, render_template
app = Flask("__name__")


@app.route('/', strict_slashes=False)
def hello():
    """ Return a given string """
    return render_template("10-hbnb_filters.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=None)
