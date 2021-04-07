from flask import Flask, render_template, request, redirect
from subprocess import Popen, PIPE, run

app = Flask(__name__)
queue = []
history = []
run(["chcp", "65001"], shell=True)
ps = Popen("cmd.exe", shell=True, stdin=PIPE, stdout=PIPE)


@app.route("/", methods=["get"])
def root():
	return render_template("main.html", list=history, length=len(history))


@app.route("/", methods=["post"])
def add_to_queue():
	command = request.form.get("string", "")
	if command != "":
		queue.append(command + "\n")
	history.append(f">>> {command}")
	return redirect("/#")


@app.route("/exec", methods=["get"])
def execute():
	global ps
	if len(queue) != 0:
		ps.stdin.write(bytes(''.join(queue), "utf-8"))
		ps.stdin.close()
		output = ps.stdout.read().decode("utf-8", "replace")
		for line in output.split("\n"):
			history.append(line)
		queue.clear()
		ps = Popen("cmd.exe", shell=True, stdin=PIPE, stdout=PIPE)
	return redirect("/#")


@app.route("/clear", methods=["get"])
def clear():
	history.clear()
	return redirect("/#")


app.run(host='0.0.0.0', debug=False)
