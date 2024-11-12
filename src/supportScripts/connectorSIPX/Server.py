import json

from flask import Flask
from flask import request
from flask import jsonify
from flask import send_from_directory
    
from flask_swagger_ui import get_swaggerui_blueprint

from Main import ElecticityPrice


app = Flask(__name__)

ep = ElecticityPrice();

swaggerui_blueprint = get_swaggerui_blueprint(
    '/API/DOCS',
    '/DOCS/API.yaml',
    config = { 'app_name': "Test application" }
)

app.register_blueprint(swaggerui_blueprint)

@app.route("/")
def Main():
    
    return "Connector SIPX"

@app.route('/DOCS/<path:path>')
def send_report(path):
    return send_from_directory('DOCS', path)
    
@app.route('/API/priceCatalog/<index>', methods=['GET'])
def getPriceCatalog(index):
    
    res = { "Name": index.upper(), "Price": ep.GetPriceCatalogSIPX() }
    
    return jsonify(res);
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)