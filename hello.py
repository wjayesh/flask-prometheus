from flask import Flask, Response
from prometheus_client import start_http_server

# from middleware import setup_metrics
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

PrometheusMetrics(app)

@app.route('/')
def hello():
    return 'Hello World'


if __name__ == "__main__":
#     # start_http_server(5000, addr="0.0.0.0")
    app.run('0.0.0.0', 5000)
