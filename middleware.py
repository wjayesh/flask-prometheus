from flask import request
import time
import sys
from prometheus_client import Counter, Histogram

APP_REQUEST_COUNT_TOTAL = Counter(
    'app_request_count_total', 'App Request Count Total',
    ['app_name', 'method', 'endpoint']
)

APP_REQUEST_COUNT_FAILED = Counter(
    'app_request_count_failed', 'App Request Count Failed',
    ['app_name', 'method', 'endpoint']
)

APP_REQUEST_COUNT_SUCCESS = Counter(
    'app_request_count_success', 'App Request Count Succeeded',
    ['app_name', 'method', 'endpoint']
)

APP_REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency',
    ['app_name', 'endpoint']
)

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    APP_REQUEST_LATENCY.labels('hw_app', request.path).observe(resp_time)
    sys.stderr.write("Response time: %ss\n" % resp_time)
    return response

def record_request_data(response):
    APP_REQUEST_COUNT_TOTAL.labels('hw_app', request.method, request.path).inc()
    
    if response.status_code is 200:
        APP_REQUEST_COUNT_SUCCESS.labels('hw_app', request.method, request.path).inc()
    else:
        APP_REQUEST_COUNT_FAILED.labels('hw_app', request.method, request.path).inc()

    sys.stderr.write("Request path: %s Request method: %s Response status: %s\n" %
            (request.path, request.method, response.status_code))
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    # The order here matters since we want stop_timer
    # to be executed first
    app.after_request(record_request_data)
    app.after_request(stop_timer)