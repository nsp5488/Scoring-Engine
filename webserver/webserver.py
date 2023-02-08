from flask import Flask, render_template, request, g

app = Flask(__name__)


services = {'8.8.8.8' : {'dns': {'service': 'dns', 'status': 'UP', 'host': '8.8.8.8'}},
'http://google.com' : {'http': {'service': 'http', 'status': 'UP', 'host': 'http://google.com'}},
'localhost': {'icmp' : {'service': 'icmp', 'status': 'UP', 'host': 'localhost'}, 'icmp': {'service': 'smtp', 'status': 'DOWN', 'host': 'localhost'}}}



@app.route("/")
def hello_world():
    return "<p> test</p>"

@app.route("/display_scores", methods=['GET'])
def display_services():
    g.services = services
    g.len = len(services)
    return render_template('index.html')


@app.route("/update_scores", methods=['POST'])
def update_services():
    print('test')
    service_info = request.form['service']
    print(service_info)
    host = service_info['host']
    service = service_info['service']
    status = service_info['status']
    print(service_info + 'in flask')

    if services.has_key(host):
        if services[host].has_key(service):
            services[host][service] = status
        else:
            services[host][service] = service_info
    else:
        services[host] = {service : service_info}
    