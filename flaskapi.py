import flask, json
from flask import request

application = app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=['GET'])
def home():
    return "<h1>Weather API</h1><p>This API returns a 10 day weather report for Vancouver.\n Data is refreshed daily.</p>"

with open('vancouverweather.json','r') as jsonfile:
    weatherreport = json.load(jsonfile)

@app.route('/', methods=['GET'])
def vancouverweather():
    return weatherreport

@app.route('/post/', methods=['POST'])
def newvancouverweatherjson():
    newweatherreport = request.get_json()
    with open('vancouverweather.json','w') as newjsonfile:
        json.dump(newweatherreport, newjsonfile)
    return "Weather Data Uploaded"
app.run()