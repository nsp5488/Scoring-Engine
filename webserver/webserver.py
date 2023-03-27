from flask import Flask, request, redirect
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

services = {}
scores = {'blue_score': 0, 'red_score' : 0}

@app.route("/")
def landing_page():
    return redirect('/display_scores')

@app.route("/display_scores", methods=['GET'])
def display_services():
    print(f"Received {request} from front-end")
    print("building response. . .")
    content = {'services': services, 'scores' : scores}
    print(scores)
    print("Returning response")
    return content


@app.route("/update_scores", methods=['POST'])
def update_scores():
    try:
        print(f"receives {request} FROM {request.host}\n\n")
        blue_score = request.form['blue_score']
        red_score = request.form['red_score']
        print(blue_score)
        print(red_score)
        scores['blue_score'] = str(blue_score)
        scores['red_score'] = str(red_score)
        print(scores)
        return {"Success":True}
    except Exception:
        return {"Success":False}


@app.route("/update_services", methods=['POST'])
def update_services():
    try:
        print(f"Received {request} FROM {request.host}\n\n")

        host = request.form['host']
        service = request.form['service']
        status = request.form['status']
        score = request.form['value']

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
