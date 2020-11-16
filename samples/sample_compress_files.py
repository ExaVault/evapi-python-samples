import datetime
import os
import sys

from dotenv import load_dotenv
from exavault import ResourcesApi
from exavault.models.compress_files_request_body import CompressFilesRequestBody

##
# sample_compress_files.py - Use the Resources API to compress files
##


##
# To use this script, add your credentials to a file named .env which is located in the same directory as this script
#
# Your API key will be the EV_KEY
# Your access token will be EV_TOKEN
# Your account URL will be the address you should use for the API endpoint
#
# To obtain your API Key and Token, you'll need to use the Developer page within the web file manager
# See https://www.exavault.com/developer/api-docs/#section/Obtaining-Your-API-Key-and-Access-Token
#
# Access tokens do not expire, so you should only need to obtain the key and token once.
#
# Your account URL is determined by the name of your account.
# The URL that you will use is https://accountname.exavault.com/api/v2/ replacing the "accountname" part with your
# account name.
# See https://www.exavault.com/developer/api-docs/#section/Introduction/The-API-URL
##

load_dotenv()
API_KEY = os.getenv('EV_KEY')
ACCESS_TOKEN = os.getenv('EV_TOKEN')
ACCOUNT_URL = os.getenv('ACCOUNT_URL')

if __name__ == "__main__":

    # We are demonstrating the use of the ResourcesApi, which is used for file operations (upload, download, delete, etc)
    #
    # For this demo, we'll create a new folder and upload some files into it. Then we'll compress some of the files into
    # a new zip file in the folder

    # We have to override the default configuration of the API object with an updated host URL so that our code
    # will reach the correct URL for the api. We have to override this setting
    # for each of the API classes we use
    resources_api = ResourcesApi()
    resources_api.api_client.configuration.host = ACCOUNT_URL

    # We will create a new folder tree for the demo. The top-level folder will
    # have a different name each time you run this script
    parent_folder = "sample_compress_{}".format(datetime.datetime.today().strftime("%s"))

    # We are uploading a sample file provided along with this script.
    # It will have a different name in the account each time it is uploaded
    filename = os.path.join(os.path.dirname(__file__), "files/ExaVault Quick Start.pdf")

    target_size = os.path.getsize(filename)

    # We'll store the IDs, which we'll grab from the responses from new
    # resource uploads, that we want to compress
    compress_resources = []

    for i in range(6):
        # We're  uploading the same file under different names to make sure we
        # have multiple files in our target folder
        target_filename = "/{}/quick start {}.pdf".format(parent_folder, i)
        try:

            # The uploadFile method of the ResourcesApi class will let us upload a file to our account
            # See https://www.exavault.com/developer/api-docs/#operation/uploadFile for the details of this method
            #
            result = resources_api.upload_file(
                API_KEY, ACCESS_TOKEN, target_filename, target_size, file=filename)

            # We want to make an archive that contains the files we've uploaded
            # The ResourcesApi.upload_file method returns a swagger_client.model.ResourceResponse object
            # The ResourceResponse.data and ResourceResponse.id attributes will give us a Resource object and the 
            # resource ID of the newly uploaded file respectively.
            compress_resources.append("id:{}".format(result.data.id))
        except Exception as e:
            print('Exception setting up files:', str(e))
            sys.exit(1)

    print("Uploaded starting files to {}".format(parent_folder))

    # If we got this far, we have a folder that contains 5 PDF files
    # Next we are going to use the same ResourcesApi to compress those files into a zip file
    # Compressing files doesn't remove the files from the account

    try:
        # We stored the resource IDs of all the files we want to compress into the compress_resources list.

        # API methods that take a JSON body, such as the compressFiles method, require us to submit an object with the
        # parameters we want to send to the API.
        # See https://www.exavault.com/developer/api-docs/#operation/compressFiles for the request body schema
        #
        # This will overwrite an existing zip file with a new one
        request_body = CompressFilesRequestBody(
            resources=compress_resources,
            parent_resource='/',
            archive_name='zipped_files.zip',
        )
        result = resources_api.compress_files(API_KEY, ACCESS_TOKEN, body=request_body)

        # The ResourcesApi.compress_files method returns a swagger_client.model.ResourceResponse object
        print("Created archive at {}".format(result.data.attributes.path))

    except Exception as e:
        print('Exception when compressing files:', str(e))
        sys.exit(4)
