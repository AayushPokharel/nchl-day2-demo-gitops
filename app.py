from flask import Flask, jsonify
import os
import json

app = Flask(__name__)

# Application state
app.healthy = True  # Used for liveness probe
app.ready = True    # Used for readiness probe

app.config['NAME'] = os.getenv('person_name')
app.config['COMPANY'] = os.getenv('company_name')

@app.route('/')
def hello_geek():
    name = app.config['NAME']
    company = app.config['COMPANY']

    return f'<h1>Hello from Flask & Docker. v1.0.0  - {name} {company}</h1>'

@app.route('/getData')
def get_data():
    try:
        with open("userdata.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/healthz/liveness')
def liveness():
    """
    Kubernetes liveness probe endpoint
    Returns:
        200 - Application is alive
        503 - Application is not alive
    """
    if app.healthy:
        return jsonify({"status": "UP"}), 200
    return jsonify({"status": "DOWN"}), 503

@app.route('/healthz/readiness')
def readiness():
    """
    Kubernetes readiness probe endpoint
    Returns:
        200 - Application is ready to serve traffic
        503 - Application is not ready to serve traffic
    """
    if app.ready:
        return jsonify({"status": "no-UP"}), 200
    return jsonify({"status": "DOWN"}), 503

if __name__ == "__main__":
    app.run(debug=True)
