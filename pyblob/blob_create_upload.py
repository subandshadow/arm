import os, uuid
import shutil
from azure.storage.blob import BlobServiceClient,PublicAccess

connection_string = 'DefaultEndpointsProtocol=https;AccountName=sa0sw7dlvivze7p4;AccountKey=Gz3ky+TXBOoomZpmATg8VRRKuj3525GLw4jlw6lE8MkrauOOnCu14ZGUmlqeYqttYeeVKEZuX07w+AStWDAGwA==;EndpointSuffix=core.windows.net'

try:
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Create a unique name for the container
    container_name = str(uuid.uuid4())
    container_name = container_name.replace('-', '')
    file = open(file='container_name', mode='w')
    file.write(container_name)
    file.close()
    
    
    # Create the container
    container_client = blob_service_client.create_container(container_name)
    container_client.set_container_access_policy({}, public_access=PublicAccess.Container)

    # Create a local directory to hold blob data
    local_path = "./data"

    # Remove if for some reason exists after last execution
    # shutil.rmtree(local_path, ignore_errors=True)
    
    os.mkdir(local_path)

    for i in range(10):
        # Create a file in the local data directory to upload and download
        local_file_name = str(uuid.uuid4()) + ".txt"
        local_file_name = local_file_name.replace('-', '')
        upload_file_path = os.path.join(local_path, local_file_name)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

        # Write text to the file
        file = open(file=upload_file_path, mode='w')
        file.write("Hello, World!")
        file.close()

        print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

        # Upload the created file
        with open(file=upload_file_path, mode="rb") as data:
            blob_client.upload_blob(data)

        print("Deleting the local source")
        os.remove(upload_file_path)

    print("\nListing blobs in container %s..." % container_name)

    # List the blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)

    # # Clean up
    # print("\nPress the Enter key to begin clean up")
    # input()

    # print("Deleting blob container...")
    # container_client.delete_container()
    
    os.rmdir(local_path)

    print("Done")

except Exception as ex:
    print('Exception:')
    print(ex)