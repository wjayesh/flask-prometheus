from flask import Flask
import os
import socket
from middleware import setup_metrics

app = Flask(__name__)

setup_metrics(app)

@app.route('/')
def hello():
    return 'Hello World from host \"%s\".\n' % socket.gethostname()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
