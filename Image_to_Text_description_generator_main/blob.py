from azure.storage.blob import BlobServiceClient
import os

conn_str = "DefaultEndpointsProtocol=https;AccountName=ecommerceblobvtryon;AccountKey=4yipKh+/7BYVwiOtxDGfivMzinvUh/nGk8p+ApFfLEDdBFAGOkHmyv3XQQE+I3vZql3OhszllRzK+AStBUQX9A==;EndpointSuffix=core.windows.net"  # from Storage Account → Access Keys
container_name = "vtryon"
local_base = "temp"  # your local folder

client = BlobServiceClient.from_connection_string(conn_str)
container = client.get_container_client(container_name)

for root, dirs, files in os.walk(local_base):
    for file in files:
        local_path = os.path.join(root, file)
        blob_path = os.path.relpath(local_path, local_base).replace("\\", "/")
        blob_client = container.get_blob_client(blob_path)
        with open(local_path, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)
            print(f"Uploaded: {blob_path}")

print("Done!")