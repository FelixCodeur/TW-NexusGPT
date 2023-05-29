import flask
from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route("/")
def main():
  return "OK"

@app.route("/kill1/")
def kill1():
    os.system("kill 1")
    
def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  run()