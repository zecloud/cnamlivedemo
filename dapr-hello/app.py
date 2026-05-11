from flask import Flask, request
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/')
def hello():
    return 'Hello Dapr!'


@app.route('/servicebus', methods=['POST'])
def servicebus_binding():
    payload = request.get_json(silent=True)
    if payload is None:
        data = request.data.decode('utf-8') if request.data else None
        logging.info('Received raw Service Bus binding data: %s', data)
    else:
        logging.info('Received Service Bus binding JSON payload: %s', payload)
    return ('', 200)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
