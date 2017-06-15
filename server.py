import datetime
import json
from flask import Flask, render_template, request, jsonify

today = datetime.date.today().isoformat()
file_name =  "resource/" + today + ".json"
css_name =  "static/style.css"
app = Flask(__name__)

@app.route('/view')
def view():
    data = read_model()
    data = write_css(data)
    if data is None:
        data = []
    return render_template('view.html', data=data)

@app.route('/api/<seat_id>', methods=['GET'])
def get(seat_id):
    model = read_model()
    if model is None:
        return "NOT FOUND"
    else:
        return jsonify(result)

@app.route('/api/<seat_id>', methods=['POST'])
def post(seat_id):
    result = set_property(seat_id)
    index = result.index(seat_id) + 1
    return "Your waiting number is {}".format(index)

@app.route('/api/<seat_id>', methods=['DELETE'])
def delete(seat_id):
    data = read_model()
    result = delete_model(seat_id, data)
    return "Your request was successfully deleted!"
    #return jsonify(result)

def set_property(seat_id):
    data = read_model()
    if data is None:
        data = []
    result = write_model(seat_id, data)
    return result

def read_model():
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except IOError as e:
        return None

def write_model(seat_id, data):
    if not seat_id in data:
        data.append(seat_id)
    try:
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)
            return data
    except IOError as e:
        print e
        return None

def delete_model(seat_id, data):
    try:
        data.remove(seat_id)
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)
            return data
    except IOError as e:
        print e
        return None
    except ValueError as e:
        return "already your request is removed"

def write_css(data):
    try:
        with open(css_name, 'w') as f:
            f.write("#table { display:table; border-collapse:separate; border-spacing: 5px 5px; \
                    margin: 20px; }\n")
            f.write("#table .row { display:table-row; }\n")
            f.write("#table .seat { display:table-cell; width:30px; height:40px; font-size: 12px; \
                    border:solid 2px black; border-radius: 5px; \
                    text-align: center; vertical-align: middle;}\n")
            f.write("#table .dummy-col { width: 10px; visibility:hidden; }\n")
            f.write("#table .dummy-row .dummy-col { height: 20px; visibility:hidden; }\n")
            if data is not None:
                if len(data) > 0:
                    f.write("#table .row #seat-{}".format(int(data[0])))
                    for seatid in data[1:]:
                        f.write(", #table .row #seat-{}".format(int(seatid)))
                    f.write(" { background-color:#ffce00; color:red; }")
        return data
    except IOError as e:
        print e
        return None

if __name__ == '__main__':
    app.debug = True 
    app.run(host='0.0.0.0')
