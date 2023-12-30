import flask
from flask_cors import CORS
from server_util import create_output_data
import time

app = flask.Flask(__name__)
CORS(app)

@app.route('/')
def index():
    print("Welcome to Qsuggest server")
    return

@app.route('/get_data', methods=['POST'])
def get_data():
    start_time = time.time()
    inp_data = flask.request.get_json()
    out_data = create_output_data(inp_data)
    
    print('Time Taken', time.time()-start_time)
    return flask.jsonify(out_data)


if __name__ == '__main__':
    app.run(debug=True)