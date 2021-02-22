import flask
from flask import Flask, render_template, request, redirect
from os import system

app = Flask(__name__)
queue = []

@app.route("/", methods = ["get"])

def root():
	return render_template("main.html", list = queue)

@app.route("/", methods = ["post"])

def combine():
	global queue
	line = request.form.get("string", None)
	if line and line != "":
		queue.append(line)
	return redirect("/")
		
@app.route("/execute")

def exec():
	global queue
	if queue != []:
		command = ""
		for i in queue:
			command += (i + " & ")
		system('cmd /c \"' + command +'\"')
		queue = []
	return redirect("/")

app.run(host='192.168.0.17',debug = False)