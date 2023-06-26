import os, uuid
import shutil
from azure.storage.blob import BlobServiceClient

source_connection_string = 'DefaultEndpointsProtocol=https;AccountName=sa0sw7dlvivze7p4;AccountKey=Gz3ky+TXBOoomZpmATg8VRRKuj3525GLw4jlw6lE8MkrauOOnCu14ZGUmlqeYqttYeeVKEZuX07w+AStWDAGwA==;EndpointSuffix=core.windows.net'
target_connection_string = 'DefaultEndpointsProtocol=https;AccountName=sa1sw7dlvivze7p4;AccountKey=WCVGvZlv/OyODrMNn6yaIK6gLrHi/y7lSO0yuKEKyNnKtk/UURCO2JXaCpaRQpVbUfeARqXzfbeq+AStqeOwRA==;EndpointSuffix=core.windows.net'

try:
    with open(file='container_name', mode="r") as container_data:
        
        container_name = container_data.read()
        
        # Create blob service clients for source and destination storage accounts
        source_blob_service_client = BlobServiceClient.from_connection_string(source_connection_string)
        target_blob_service_client = BlobServiceClient.from_connection_string(target_connection_string)

        # Get the source container client
        source_container_client = source_blob_service_client.get_container_client(container_name)
        target_container_client = target_blob_service_client.create_container(container_name)
        
        # List all blobs in the source container
        source_blobs = source_container_client.list_blobs()

        # Copy each blob to the destination container
        for blob in source_blobs:
            source_blob_client = source_blob_service_client.get_blob_client(container_name, blob.name)
            target_blob_client = target_blob_service_client.get_blob_client(container_name, blob.name)
            target_blob_client.start_copy_from_url(source_blob_client.url)

            print(f"Copying blob {blob.name}...")

        print("Blob copy completed!")

except Exception as ex:
    print('Exception:')
    print(ex)