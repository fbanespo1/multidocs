from flask import Flask, request, jsonify
import os
import requests
from azure.cognitiveservices.search.searchclient import SearchClient
from msrest.authentication import CognitiveServicesCredentials
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Initialize Azure and OpenAI credentials
AZURE_SEARCH_KEY = os.getenv('AZURE_SEARCH_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SEARCH_SERVICE_NAME = os.getenv('SEARCH_SERVICE_NAME')
SEARCH_INDEX_NAME = os.getenv('SEARCH_INDEX_NAME')
BLOB_CONNECTION_STRING = os.getenv('BLOB_CONNECTION_STRING')

@app.route('/list_blobs', methods=['GET'])
def list_blobs():
    container_name = request.args.get('container_name')
    # Code to list blobs from Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(container_name)
    
    blob_list = [blob.name for blob in container_client.list_blobs()]
    return jsonify(blob_list)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    # Code to search blobs using Azure Cognitive Search
    search_url = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/indexes/{SEARCH_INDEX_NAME}/docs"
    headers = {'api-key': AZURE_SEARCH_KEY, 'Content-Type': 'application/json'}
    params = {'search': query}
    
    response = requests.get(search_url, headers=headers, params=params)
    search_results = response.json()
    return jsonify(search_results)

@app.route('/summarize', methods=['POST'])
def summarize():
    content = request.json.get('content')
    # Code to summarize content using OpenAI
    openai_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {'Authorization': f'Bearer {OPENAI_API_KEY}', 'Content-Type': 'application/json'}
    data = {
        'prompt': f'Summarize: {content}',
        'max_tokens': 100
    }
    
    response = requests.post(openai_url, headers=headers, json=data)
    summary = response.json()
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)
