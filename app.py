pip install flask azure-storage-blob
from flask import Flask, render_template, request, send_file
from azure.storage.blob import BlobServiceClient, BlobClient

# Azure Blob Storage configuration
CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=arnabsa;AccountKey=GlWpxAlG70eELtWZaz0FrbYyZqLGApX9tSxNLCSDDSjbdYsgbRMYCL/IlSFRQFf5mVcBKPno7XoZ+AStsx90rA==;EndpointSuffix=core.windows.net'
CONTAINER_NAME = 'azureml'

app = Flask(__name__)

# Initialize Azure Blob Storage client
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return 'No file selected'

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return 'No file selected'

    # Upload the file to Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)
    blob_client.upload_blob(file)

    return 'File uploaded successfully'

@app.route('/download/<filename>')
def download(filename):
    # Download the file from Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=filename)
    file_stream = blob_client.download_blob().readall()

    return send_file(
        file_stream,
        mimetype=blob_client.blob_properties.content_type,
        as_attachment=True,
        attachment_filename=filename
    )

if __name__ == '__main__':
    app.run(debug=True)
