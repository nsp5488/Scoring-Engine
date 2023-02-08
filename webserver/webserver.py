from flask import Flask, request, redirect
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

services = {}

@app.route("/")
def landing_page():
    return redirect('/display_scores')

@app.route("/display_scores", methods=['GET'])
def display_services():
    print(f"Received {request} from front-end")
    return services


@app.route("/update_scores", methods=['POST'])
def update_services():
    try:
        print(f"Received {request} FROM {request.host}")

        host = request.form['host']
        service = request.form['service']
        status = request.form['status']

        if host in services.keys():
            if service in services[host].keys():
                services[host][service] = status
            else:
                services[host][service] = status
        else:
            services[host] = {service : status}
        return {'Success': True}
    except Exception:
        return {'Success' : False}