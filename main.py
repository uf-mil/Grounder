#!/usr/bin/env python
import os
from glob import glob
from flask import Flask, Response, request, render_template, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from jsonschema import validate
import json
import shutil

# To change the default port and host, modify the following variables: 
PORT = 5000
HOST = '0.0.0.0'
UPLOAD_LIMIT = None
CURRENT_UPLOAD_SIZE = 0
'''
The following template is the standard format we export as json files. Each json file must have at least one label.
The label is a json object that contains a class which is what the label is classified as. 
The class comes from the template file set up by the user and exported in json format. Inside is a list of acceptable classes. 
Each label requires a minimum of three points in order to form a shape. This may cause some errors as our current labeler allows for users to try 
and submit labels with fewer than three. These are rejected but there is no indication that such a rejection occurred. 
'''
EXPORT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-06/schema#",
    "title": "Export Schema",
    "type": "array",
    "items": {
    	"type":"object",
    	"properties":{
	        "label":
	        {
	            "description" : "Contains the class for our label.",
	            "type": "object",
	            "properties":
	            {
	                "class": {"type" : "string"}
	            },
	            "required":["class"]
	        },
	        "points" :
	        {    
	            "description": "Contains the points that make up the label.",
	            "type": "array",
	            "items":
	            {
	            	"type":"object",
	            	"properties":{
	                	"x":{"type":"number"},
	                	"y":{"type":"number"}
	            	},
	            	"required":["x","y"]
	            },
	            "minItems": 3
	            
	        },
	    },
	    "required": ["label", "points"]
	},
	"minItems":1
}
# Another schema, this one checks those trying to upload a template. Here we ensure there is at least one class present for labeling. 
TEMPLATE_SCHEMA = {
	    "$schema": "http://json-schema.org/draft-06/schema#",
    "title": "Template Schema",
    "type": "object",
    "properties": {
        "classes":
        {
            "description" : "Contains all possible classes for label.",
            "type": "array",
            "items":
            {
            	"type":"string"
            },
            "minItems":1
        }
    },
    "required": ["classes"]
}

app = Flask(__name__, static_url_path='/static')

if 'port' in os.environ:
    PORT = int(os.environ['port'])
if 'host' in os.environ:
    HOST = os.environ['host']
if 'upload_limit' in os.environ:
    UPLOAD_LIMIT = int(os.environ['upload_limit'])

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
        global CURRENT_UPLOAD_SIZE
        global UPLOAD_LIMIT
        if UPLOAD_LIMIT is not None and CURRENT_UPLOAD_SIZE >= UPLOAD_LIMIT:
            return Response(status=400, response='Reached upload limit')
        check = os.path.isfile(os.path.join('static/data/', (my_path + '.png')))
        if check == False:
            return Response(status=400, response='Image does not exist.')
        with open(os.path.join('static/data/', (my_path + '.json')), "w+") as outfile:
            data = request.get_json()
            print(data)
            try:
                validate(data, EXPORT_SCHEMA)
            # print(v)
            except:
                return Response(status=400, response='Json does not match the required format, requires 3 points minimum and 1 label.')
            # Find the template for this folder
            template = fetch_template(os.path.join('static/data/',(my_path[:my_path.rindex('/')] + '/template.json')))
            if template == None:
                return Response(status=400, response='Unable to find template.')
            # Open the template
            template = open(os.path.join(template, 'template.json'), 'r')
            # Convert the template json to something validate can understand.
            template = json.load(template)
            for dict_json in data:
                try:
                    if dict_json['label']['class'] not in template['classes']:
                        # print(dict_json['label']['class'])
                        return Response(status=400, response='Selected class not available in template.')
                except:
                    # If classes is not found in template then we error out. So this is an exra layer of security that shouldn't be necessary.
                    return Response(status=400, response='Unable to find keyword: classes')
            json.dump(data, outfile, sort_keys=True, indent=4)
        if UPLOAD_LIMIT is not None:
            CURRENT_UPLOAD_SIZE = CURRENT_UPLOAD_SIZE + 1
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
        return Response(status=400, response='directory does not exist')
    if len(request.files) != 1:
        return Response(status=400, response='1 file must be uploaded')
    global CURRENT_UPLOAD_SIZE
    global UPLOAD_LIMIT
    if UPLOAD_LIMIT is not None and CURRENT_UPLOAD_SIZE >= UPLOAD_LIMIT:
        return Response(status=400, response='Reached upload limit')
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
    if UPLOAD_LIMIT is not None:
        CURRENT_UPLOAD_SIZE = CURRENT_UPLOAD_SIZE + 1
    return Response(status=200)

@app.route('/api/next/', methods=['GET'])
@app.route('/api/next/<path:my_path>', methods=['GET'])
def next(my_path=''):
    path = os.path.join('static/data', my_path)
    if not os.path.isdir(path):
        return Response(status=400, response='not a directory')
    for filename in os.listdir(path):
        # Find the image and make sure it isn't already labelled
        # print(os.path.join(os.path.splitext(file)[0], '.json'))
        resolved = os.path.join(path, filename)
        split = os.path.splitext(resolved)
        if split[1] == '.png' and not os.path.isfile(split[0] + '.json'):
            return os.path.splitext(filename)[0]
    return Response(status=404, response='')

@app.route('/api/dir/', methods=['GET', 'POST'])
@app.route('/api/dir/<path:my_path>', methods=['GET', 'POST'])
def api_dir(my_path=''):
    if request.method == 'POST':
        global CURRENT_UPLOAD_SIZE
        global UPLOAD_LIMIT
        if UPLOAD_LIMIT is not None and CURRENT_UPLOAD_SIZE >= UPLOAD_LIMIT:
            return Response(status=400, response='Reached upload limit')
        my_path = os.path.join('static/data/', my_path)
        os.makedirs(my_path)
        if UPLOAD_LIMIT is not None:
            CURRENT_UPLOAD_SIZE = CURRENT_UPLOAD_SIZE + 1
        return 'Directory Created.'
        # do_edit_dir()
    else:
        my_path = os.path.join('static/data/', my_path)
        if os.path.isdir(my_path):
            child_dirs = [name for name in os.listdir(
                my_path) if os.path.isdir(os.path.join(my_path, name))]
            child_imgs = [os.path.splitext(name)[0] for name in os.listdir(
                my_path) if os.path.isfile(os.path.join(my_path, name)) and name.endswith('.png')]
            # print(my_path)
            dicti = {'children': child_dirs, 'images': child_imgs}
            return jsonify(dicti)
        else:
            return Response(status=400, response='Unable to find path')

@app.route('/api/template/', methods=['GET', 'POST'])
@app.route('/api/template/<path:my_path>', methods=['GET', 'POST'])
def api_template(my_path=''):
    if request.method == 'GET':
        my_path = os.path.join('static/data/', my_path)
        my_path = fetch_template(my_path)
        if my_path == None:
            return Response(status=400, response='Unable to find template.')
        with open(os.path.join(my_path, 'template.json'), 'r') as f:
            return json.dumps(json.load(f)), 200, {'ContentType': 'application/json'}
    elif request.method == 'POST':
        global CURRENT_UPLOAD_SIZE
        global UPLOAD_LIMIT
        if UPLOAD_LIMIT is not None and CURRENT_UPLOAD_SIZE >= UPLOAD_LIMIT:
            return Response(status=400, response='Reached upload limit')
        with open(os.path.join('static/data/', my_path,  'template.json'), "w+") as outfile:
            data = request.get_json()
        # Call the validate function from jsonschema to verify our output json conforms with the template we were supposed to create
            try:
                validate(data, TEMPLATE_SCHEMA)
            except:
                return Response(status=400, response='Invalid template, requires at least 1 label and proper formatting. Refer to schema.')
            json.dump(request.get_json(), outfile, sort_keys=True, indent=4)
        if UPLOAD_LIMIT is not None:
            CURRENT_UPLOAD_SIZE = CURRENT_UPLOAD_SIZE + 1
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

def fetch_template(my_path):
    iterations = 0
    while not os.path.isfile(os.path.join(my_path, 'template.json')):
            my_path = os.path.normpath(os.path.join(my_path, '../'))
            # print(my_path)
            iterations = iterations + 1
            if my_path== 'static' or iterations == 500:
                return None
    return my_path

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
