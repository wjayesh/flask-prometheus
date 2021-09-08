from flask import Flask, Response
# from middleware import setup_metrics
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)

@app.route('/')
def hello():
    return 'Hello World'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
