import datetime
import os
import sys

from dotenv import load_dotenv
from exavault import ResourcesApi


##
# sample_upload_files.py - Use the ResourcesApi to upload a file to your account
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
#   account name
# See https://www.exavault.com/developer/api-docs/#section/Introduction/The-API-URL
##

load_dotenv()
API_KEY = os.getenv('EV_KEY')
ACCESS_TOKEN = os.getenv('EV_TOKEN')
ACCOUNT_URL = os.getenv('ACCOUNT_URL')

if __name__ == "__main__":

    # We are demonstrating the use of the ResourcesApi, which can be used to
    # manage files and folders in your account
    #
    # For this demo, we'll upload a file found in the same folder as this sample code.
    #
    # We are going to upload the file as a different name each time so that it is obvious that the file is being upload
    # There are parameters to control whether files can be overwritten by repeated uploads
    #
    # We have to override the default configuration of the API object with an updated host URL so that our code
    # will reach the correct URL for the api. We have to override this setting
    # for each of the API classes we use
    resources_api = ResourcesApi()
    resources_api.api_client.configuration.host = ACCOUNT_URL

    try:

        # We are uploading a sample file provided along with this script.
        # It will have a different name in the account each time it is uploaded
        filename = os.path.join(
            os.path.dirname(__file__), "files/dog.jpg")
        target_filename = 'dog_{}.jpg'.format(datetime.datetime.today().strftime("%Y%m%d_%H%M%S"))
        target_size = os.path.getsize(filename)

        # The uploadFile method of the ResourcesApi class will let us upload a file to our account
        # See https://www.exavault.com/developer/api-docs/#operation/uploadFile for the details of this method
        #
        result = resources_api.upload_file(API_KEY, ACCESS_TOKEN, target_filename, target_size, file=filename)

        # The uploadFile method of the ResourcesApi returns a swagger_client.model.ResourceResponse object
        # See https://www.exavault.com/developer/api-docs/#operation/uploadFile
        # for the details of the response object

        # Verify that the uploaded file's reported size matches what we expected.
        # The getAttributes method of the ResourceResponse object will let us get the details of the file
        size_uploaded = result.data.attributes.size

        if size_uploaded != target_size:
            print(
                "Uploaded file does not match expected size. Should be {} but is {}".format(
                    target_size,
                    size_uploaded))
            sys.exit(3)

        # Success!
        print("Uploaded {}".format(result.data.attributes.path))

    except Exception as e:
        # If there was a problem, such as our credentials not being correct or not having upload permissions,
        # there will be an exception thrown.
        print('Exception when calling ResourcesApi.uploadFile: ', str(e))
        sys.exit(1)
