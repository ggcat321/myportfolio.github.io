# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:57:45 2024

@author: crazy
"""
from flask import Flask
from flask import request

from flask import render_template

app = Flask(__name__)

@app.route("/getname", methods=['GET'])
def getname():
    name = request.args.get('name')
    fruit =request.args.get('fruit')
    return render_template('index.html',**locals())
if __name__ == "__main__":
    app.run()
