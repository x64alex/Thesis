from flask import Flask, request, jsonify
from flask_cors import CORS
from JCML.interpret import JCML

app = Flask(__name__)
CORS(app)

jcml = JCML('JCML/chatConfiguration.json')

@app.route('/-/healthy', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    user_input = data.get('user_input')
    response = jcml.get_response(user_input)
    return jsonify({'response': response}), 200, {'Access-Control-Allow-Origin': 'https://investmentchatbot.netlify.app'}

@app.route('/update_json', methods=['POST'])
def update_json():
    data = request.json
    jcml.update_configuration(data)
    return jsonify({'message': 'JSON file updated successfully'}), 200, {'Access-Control-Allow-Origin': 'https://investmentchatbot.netlify.app/'}

