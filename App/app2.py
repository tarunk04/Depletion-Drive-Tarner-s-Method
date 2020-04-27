from flask import Flask,render_template, jsonify, redirect, url_for, request
import os
from utils import *
app = Flask(__name__)

raw_data = None
# @app.route('/success/<name>')
# def success(name):
#    return 'welcome %s' % name

# @app.route('/login')
# def login():
#    if request.method == 'POST':
#       user = request.form['nm']
#       return redirect(url_for('success',name = user))
#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))
@app.route('/solve/',methods=['POST'])
def solve():
    global raw_data
    try:
        raw_data = calculate(raw_data)
        raw = raw_data
        processed_data = {}
        for k in raw['data'].keys():
            # print(list(raw['data'][k]))
            if type(raw['data'][k]) == np.ndarray:
                processed_data[k] = list(np.float64(raw['data'][k]))
            else:
                processed_data[k] = raw['data'][k]
        processed_data['name'] = raw['name']
        return jsonify(processed_data)
        return jsonify(raw_data)
    except:
        return jsonify(0)

@app.route('/update/',methods=['POST'])
def update():
    data = request.get_json()
    global raw_data
    if data['key'] == 'name':
        raw_data['name'] = data['val']
    else:
        print(raw_data['data'][data['key']])
        if data['type'] == 'single':
            raw_data['data'][data['key']] = np.float64(data['val'])
        elif data['type'] == 'array':
            try:
                raw_data['data'][data['key']] = np.float64(data['val'].rstrip("\n").split('\n'))
            except:
                raw_data['data'][data['key']] = None
            # print(np.float64(data['val'].split('\n')))
        print(raw_data['data'][data['key']])
    return "working"


@app.route('/open/',methods=['POST'])
def open():
    save_files = os.listdir('save/')
    return jsonify(save_files)

@app.route('/save/',methods=['POST'])
def save():
    global raw_data
    try:
        save_data(raw_data)
        return jsonify(1)
    except:
        return jsonify(0)


@app.route('/load/',methods=['POST'])
def load():
    data = request.get_json()
    # print(data['file'])
    raw = load_reservoir(data['file'])
    global raw_data
    raw_data = raw
    # print(raw['data'].keys())
    processed_data = {}
    for k in raw['data'].keys():
        # print(list(raw['data'][k]))
        if type(raw['data'][k]) == np.ndarray:
            processed_data[k] = list(np.float64(raw['data'][k]))
        else :
            processed_data[k] = raw['data'][k]
    processed_data['name'] = raw['name']
    return jsonify(processed_data)

@app.route('/create/',methods=['POST'])
def create():
    raw = load_reservoir("template.save",path="template/")
    global raw_data
    raw_data = raw
    return "Working"

@app.route('/api/',methods=['POST'])
def api():
    data = request.get_json()
    print(data['Api_id'])
    return redirect(url_for(data['Api_id']),code=307)


@app.route('/')
def home():
    return render_template('/index.html')


if __name__ == '__main__':
   app.run(debug = True)