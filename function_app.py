import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="helloworld", auth_level=func.AuthLevel.ANONYMOUS)
def helloworld(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.service_bus_queue_trigger(arg_name="msg", queue_name="cnammessage", connection="ServiceBusConnectionString")
def sbqtriggerfunc(msg: func.ServiceBusMessage):
    logging.info('Python ServiceBus queue trigger processed message: %s', msg.get_body().decode('utf-8'))



@app.blob_trigger(arg_name="myblob", path="test",
                               connection="BlobStorageConnectionString") 
def reactblobfunc(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")


# This example uses SDK types to directly access the underlying BlobClient object provided by the Blob storage trigger.
# To use, uncomment the section below and add azurefunctions-extensions-bindings-blob to your requirements.txt file
# Ref: aka.ms/functions-sdk-blob-python
#
# import azurefunctions.extensions.bindings.blob as blob
# @app.blob_trigger(arg_name="client", path="test",
#                   connection="BlobStorageConnectionString")
# def reactblobfunc(client: blob.BlobClient):
#     logging.info(
#         f"Python blob trigger function processed blob \n"
#         f"Properties: {client.get_blob_properties()}\n"
#         f"Blob content head: {client.download_blob().read(size=1)}"
#     )



@app.queue_trigger(arg_name="azqueue", queue_name="filedemessage",
                               connection="BlobStorageConnectionString") 
# @app.blob_input(arg_name="inputblob", path="test/{name}",
#                 connection="BlobStorageConnectionString")
@app.blob_output(arg_name="outputblob", path="test/{rand-guid}.txt",
                connection="BlobStorageConnectionString")
@app.service_bus_queue_output(arg_name="sbqueue", queue_name="cnammessage", connection="ServiceBusConnectionString")
def hellofile(azqueue: func.QueueMessage, outputblob: func.Out[str], sbqueue: func.Out[str]):
    logging.info('Python Queue trigger processed a message: %s',
                azqueue.get_body().decode('utf-8'))
    outputblob.set(azqueue.get_body().decode('utf-8'))
    sbqueue.set(azqueue.get_body().decode('utf-8'))
