from flask import Flask, jsonify, request, send_from_directory
import json
app = Flask(__name__)

with open("map_boxes", "r") as f:
    boxes = json.load(f)

app = Flask(__name__, static_url_path='', static_folder='.')  

# serve the html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# serve the box data
@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(boxes)

# add text to the boxes
@app.route('/update_text', methods=['POST'])
def update_text():
    data = request.json
    index = data['index']
    text = data['text']
    if index is not None and 0 <= index < len(boxes):
        boxes[index] = (*boxes[index][:4], text) 
        _save_to_file()
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid index"})

# remove outlier boxes
@app.route('/delete_box', methods=['POST'])
def delete_box():
    data = request.json
    index = data['index']
    del boxes[index]
    _save_to_file()
    return jsonify({"status": "success"})

def _save_to_file():
    with open("bounding_boxes.json", "w") as f:
        json.dump(boxes, f)

if __name__ == '__main__':
    app.run(debug=True)
