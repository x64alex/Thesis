from flask import Flask, request, jsonify
from flask_cors import CORS
from JCML.interpret import JCML

app = Flask(__name__)
CORS(app)
jcml = JCML('JCML/chatConfiguration.json')
    
@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    user_input = data.get('user_input')
    response = jcml.get_response(user_input)
    return jsonify({'response': response})

@app.route('/update_json', methods=['POST'])
def update_json():
    data = request.json
    jcml.update_configuration(data)

    return jsonify({'message': 'JSON file updated successfully'})
if __name__ == '__main__':
    app.run()