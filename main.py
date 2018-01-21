#!/usr/bin/env python
import os
from glob import glob
from flask import Flask, Response, request, render_template, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import json


UPLOAD_FOLDER = '/data'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_url_path='/static')
port = 5000
host = '0.0.0.0'
if 'port' in os.environ:
    port = int(os.environ['port'])
if 'host' in os.environ:
    host = os.environ['host']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/<path:file>')
def statics(file):
    return app.send_static_file(file)


@app.route('/api/img/<path:my_path>', methods=['GET', 'POST'])
def img_open(my_path=None):
    if request.method == 'GET':
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
            return json.dumps({json.load(f)}), 200, {'ContentType': 'application/json'}


@app.route('/api/upload/<path:my_path>', methods=['GET', 'POST'])
def api_data(my_path=None):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
            <p><input type=file name=file>
            <input type=submit value=Upload>
        </form>
        '''

    else:
        return my_path if my_path is not None else 'No path'


@app.route('/api/dir/')
@app.route('/api/dir/<path:my_path>', methods=['GET', 'POST'])
def api_dir(my_path=''):
    if request.method == 'POST':
        return 'General Kenobi!'
        # do_edit_dir()
    else:
        my_path = os.path.join('static/data/', my_path)
        if os.path.isdir(my_path):
            child_dirs = [name for name in os.listdir(
                my_path) if os.path.isdir(os.path.join(my_path, name))]
            child_imgs = [os.path.splitext(name)[0] for name in os.listdir(
                my_path) if os.path.isfile(os.path.join(my_path, name))]
            print(my_path)
            dicti = {'children': child_dirs, 'images': child_imgs}
            return jsonify(dicti)
        else:
            return 'GENERAL KENOBI!'


@app.route('/json/<path:my_path>', methods=['GET', 'POST'])
def api_json():
    if request.method == 'POST':
        # do_edit_json()
        return 'General Kenobi!'
    else:
        return send_from_directory('view', my_path)
        # response = requests.get('/view/<path:my_path>')
        # response_json = jsonify(all=response.text)
        # return render_template(
        #   'results.html',
        #   form=ReqForm(request.form),
        #   response=response_json,
        #   date=datetime.datetime.now()
        # )

if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)
