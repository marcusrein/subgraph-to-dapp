from flask import Flask, render_template, request
from dotenv import load_dotenv
from json2html import *
import requests
import json
import os
 
app = Flask(__name__)
if __name__ == '__main__':
   app.run()

@app.route("/", methods=["GET", "POST"])
def index():
    swapInputNumberData = request.form["topSwapNumberInputHTML"]

    return render_template('index.html')
