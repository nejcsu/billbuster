import json

from flask import Flask
from flask import request
from flask import jsonify

from Main import ElecticityPrice


app = Flask(__name__)

ep = ElecticityPrice();

@app.route("/")
def Main():
    
    return "Connector SIPX"

@app.route('/priceCatalog/<index>', methods=['GET'])
def getPriceCatalog(index):
    
    res = { "Name": index.upper(), "Price": ep.GetPriceCatalogSIPX() }
    
    return jsonify(res);
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)    