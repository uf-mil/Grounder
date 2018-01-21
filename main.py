#!/usr/bin/env python
import os
from glob import glob
from flask import Flask, Response, request, render_template, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import json
import shutil

# To change the default port and host, modify the following variables: 
PORT = 5000
HOST = '0.0.0.0'

app = Flask(__name__, static_url_path='/static')

if 'port' in os.environ:
    PORT = int(os.environ['port'])
if 'host' in os.environ:
    HOST = os.environ['host']

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/<path:file>')
def statics(file):
    return app.send_static_file(file)

@app.route('/api/img/<path:my_path>', methods=['GET'])
def img_open(my_path=None):
    return app.send_static_file(os.path.join('data/', (my_path + '.png')))


@app.route('/api/label/<path:my_path>', methods=['GET', 'POST'])
def api_label(my_path=None):
    if request.method == 'POST':
        with open(os.path.join('static/data/', (my_path + '.json')), "w+") as outfile:
            json.dump(request.get_json(), outfile, sort_keys=True, indent=4)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    elif request.method == 'GET':
        file = os.path.join('static/data/', (my_path + '.json'))
        if not os.path.isfile(file):
            return Response(status=404, mimetype='application/json')
        with open(file, 'r') as f:
            return json.dumps(json.load(f)), 200, {'ContentType': 'application/json'}

@app.route('/api/upload/', methods=['POST'])
@app.route('/api/upload/<path:my_path>', methods=['POST'])
def api_upload(my_path=''):
    path = os.path.join('static/data', my_path)
    if not os.path.isdir(path):
        return Response(status=400, response='directory does not exsist')
    if len(request.files) != 1:
        return Response(status=400, response='1 file must be uploaded')
    f = request.files.get(list(request.files.keys())[0])
    filename = f.filename
    filename = os.path.split(filename)[-1]
    ext = os.path.splitext(filename)[1]
    if ext != '.png':
        return Response(status=400, response='file must be .png')
    # Save image
    resolved = os.path.join('static/data', my_path, filename)
    with open(resolved, 'wb') as writefile:
        f.save(writefile)
    return Response(status=200)

@app.route('/api/next/', methods=['GET'])
@app.route('/api/next/<path:my_path>', methods=['GET'])
def next(my_path=''):
    if os.path.isdir(os.path.join('static/data', my_path)):
        iteration = 0
        for file in os.listdir(os.path.join('static/data', my_path)):
            # Find the image and make sure it isn't already labelled
            # print(os.path.join(os.path.splitext(file)[0], '.json'))
            if file.endswith('.png') and (os.path.isfile(os.path.join(os.path.splitext(file)[0], '.json')) == False):
                return os.path.splitext(file)[0]
    return 'Ah, General Kenobi!'

@app.route('/api/dir/', methods=['GET', 'POST'])
@app.route('/api/dir/<path:my_path>', methods=['GET', 'POST'])
def api_dir(my_path=''):
    if request.method == 'POST':
        my_path = os.path.join('static/data/', my_path)
        os.makedirs(my_path)
        return 'Directory Created.'
        # do_edit_dir()
    else:
        my_path = os.path.join('static/data/', my_path)
        if os.path.isdir(my_path):
            child_dirs = [name for name in os.listdir(
                my_path) if os.path.isdir(os.path.join(my_path, name))]
            child_imgs = [os.path.splitext(name)[0] for name in os.listdir(
                my_path) if os.path.isfile(os.path.join(my_path, name)) and name.endswith('.png')]
            print(my_path)
            dicti = {'children': child_dirs, 'images': child_imgs}
            return jsonify(dicti)
        else:
            return 'GENERAL KENOBI!'

@app.route('/api/template/', methods=['GET', 'POST'])
@app.route('/api/template/<path:my_path>', methods=['GET', 'POST'])
def api_template(my_path=''):
    if request.method == 'GET':
        my_path_temp = os.path.join('data/', my_path)
        flag = os.path.isfile(os.path.join('data/', my_path, 'template.json'))
        if flag:
            return app.send_static_file(os.path.join('data/', my_path , 'template.json'))
        else:
            iterations =  0
            while flag is False:
                my_path_temp = os.path.join(my_path_temp, '../')
                flag = os.path.isfile(os.path.join('data/', my_path_temp, 'template.json'))
                iterations = iterations + 1
                if iterations == 3:
                    return 'Failure'
            shutil.copy2(my_path_temp, os.path.join('data/', my_path))
            return os.path.join('data/', my_path, 'template.json')
        
    elif request.method == 'POST':
        with open(os.path.join('static/data/', my_path,  'template.json'), "w+") as outfile:
            json.dump(request.get_json(), outfile, sort_keys=True, indent=4)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}



if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
