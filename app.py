from flask import Flask, render_template
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')