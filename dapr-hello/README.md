# Dapr Hello (Service Bus binding example)

This small example contains a minimal Flask app and a Dapr component that demonstrates an input binding for Azure Service Bus queues.

Files:

- `app.py` - Flask app that responds to `GET /` and accepts Dapr binding POSTs on `POST /servicebus`.
- `Dockerfile` - container image for the app.
- `components/servicebus-binding.yaml` - Dapr component for the Azure Service Bus queue binding. Replace the `<SERVICE_BUS_CONNECTION_STRING>` placeholder with your connection string.

Run locally (without Docker):

1. Install dependencies in a virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r dapr-hello/requirements.txt
```

2. Update `dapr-hello/components/servicebus-binding.yaml` with your Service Bus connection string.

3. Start the app with Dapr (standalone):

```bash
dapr run --app-id dapr-hello --app-port 5000 --components-path ./dapr-hello/components -- python dapr-hello/app.py
```

The binding will POST incoming queue messages to `http://localhost:5000/servicebus`.

Build and run the container with Dapr (optional):

```bash
docker build -t dapr-hello:latest ./dapr-hello
dapr run --app-id dapr-hello --app-port 5000 --components-path ./dapr-hello/components -- docker run --rm -p 5000:5000 dapr-hello:latest
```
