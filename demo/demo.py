from flask import Flask, request, render_template, redirect
import os
import sys

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def button():
    if request.method == "POST":
        os.system("sudo docker run -itd -p 5000:5000 grounder ./root/start.sh 0.0.0.0 5000")
        return redirect("http://ec2-34-238-117-47.compute-1.amazonaws.com:5000")
    return render_template("button.html")

if __name__ == '__main__':
     if len(sys.argv) == 3:
        app.run(debug=True,host=sys.argv[1],port=int(sys.argv[2]))
     else:
        print("Usage: demo.py <ip> <port>")   
