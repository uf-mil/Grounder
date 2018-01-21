from flask import Flask, request, render_template, redirect
import os
import sys
import time
import docker

client = docker.from_env()

app = Flask(__name__)
ports = [0] * 1000

@app.route('/', methods=["GET", "POST"])
def button():
    if request.method == "POST":
    	port = 5000

    	#Search for an unused port
    	for i in range(5000,6000):
    		if ports[i-5000] == 0:
    			port = i
    			break

        # Launch the docker container
        ports[port-5000] = client.containers.run("groundr", detach=True, command="./root/start.sh 0.0.0.0 " + str(port), ports={str(port) + '/tcp': str(port)})
        time.sleep(1.5)

        # Redirect the user to the newly launched docker container
        return redirect("http://ec2-34-238-117-47.compute-1.amazonaws.com:" + str(port))
    return render_template("button.html")

if __name__ == '__main__':
     if len(sys.argv) == 3:
        app.run(debug=True,host=sys.argv[1],port=int(sys.argv[2]))
     else:
        app.run(debug=True,host='0.0.0.0',port=80)
