# Scoring Engine

This scoring engine was written for use in a Red Vs. Blue Cyber competition at Rochester Institute of Technology

## Quick start 

### Installation

Installation of prerequisites can be done manually via pip, or by executing
```bash
ansible-playbook install_SCORE.yml
```
After executing this script, the prerequesites should be installed and you'll be ready to begin running the scoring engine.

### Determine the services to score

In the services.csv file, add the services by name that you would like to have scored, as well as the relevant IP address of the machine that the service should run on, the value of that service, and the port of the service, if it isn't running on the default port.

### Begin scoring

First, start the webserver:
```bash
flask --app ./webserver/webserver.py run
```
Then, when the competition is ready to begin, execute
```bash
python3 main.py
```
Finally, execute
```bash
npx serve .
```
in the frontend directory.

At this point, the scores, as well as the currently live services, should be visible on the frontend at http://localhost/

