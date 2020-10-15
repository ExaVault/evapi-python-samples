import datetime
import os
import sys

from dotenv import load_dotenv
from swagger_client.api.resources_api import ResourcesApi
from swagger_client.api.shares_api import SharesApi


##
# sample_shared_folder.py - Use the SharesApi to create a shared folder with a password
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

    # We are demonstrating the use of the SharesApi, which is used for managing shared folders and receives,
    # as well as for sending files. See our Sharing 101 documentation at
    # https://www.exavault.com/docs/account/05-file-sharing/00-file-sharing-101

    # For this demo, we'll create a share for a new folders. If you have an existing file or folder that you want to use
    # for the share, you won't need this step where we use the ResourcesApi to create the folders first.
    #
    # We have to override the default configuration of the API object with an updated host URL so that our code
    # will reach the correct URL for the api. We have to override this setting
    # for each of the API classes we use
    resources_api = ResourcesApi()
    resources_api.api_client.configuration.host = ACCOUNT_URL

    try:
        # We will create a new folder for the demo. The folder will have a
        # different name each time you run this script
        folder_path = "/sample_share_{}".format(datetime.datetime.today().strftime("%s"))

        # API methods that take a JSON body, such as the add_folder method, require us to submit an object with the
        # parameters we want to send to the API. This call requires a single parameter path
        request_body = {'path': folder_path}

        # We have to pass the API_KEY and ACCESS_TOKEN with every API call.
        result = resources_api.add_folder(API_KEY, ACCESS_TOKEN, body=request_body)

        # The addFolder method of the ResourcesApi returns a swagger_client.model.ResourceResponse object
        # See https://www.exavault.com/developer/api-docs/#operation/addFolder for
        # the details of the response object
        print("Created new folder {}".format(result.data.attributes.path))

    except Exception as e:
        print('Exception when calling ResourcesApi.addFolder:', str(e))
        sys.exit(1)

    # If we got this far without the program ending, we were able to set up our folder
    # and now we can use the SharesApi to share the folder.
    #
    # We have to override the default configuration of the API object with an updated host URL so that our code
    # will reach the correct URL for the api.
    shares_api = SharesApi()
    shares_api.api_client.configuration.host = ACCOUNT_URL

    try:

        # API methods that take a JSON body, such as the addShare method, require us to submit an object with the
        # parameters we want to send to the API.
        # See https://www.exavault.com/developer/api-docs/#operation/addShare for the request body schema

        # - We want to add a password to our folder
        # - We are also going to allow visitors to upload and download
        # - Note that the folder_path variable contains the full path to the folder that was created earlier
        # - We could also have pulled the ID for the new folder out of the ResourceResponse object and used that
        #   as a resource identifier here. For example, if the ID of the new folder is 23422, we could pass
        #   id:23422 in the resource parameter of this call.
        request_body = {
            'type': 'shared_folder',
            'name': 'share',
            'access_mode': [
                'download',
                'upload'
            ],
            'resources': [
                folder_path
            ],
            'action': 'download',
            'password': '99drowssaP?'
        }

        # We have to pass the API_KEY and ACCESS_TOKEN with every API call.
        result = shares_api.add_share(API_KEY, ACCESS_TOKEN, body=request_body)

        # The SharesApi::addShare method returns a swagger_client.model.RegularShareResponse object
        #  See https://www.exavault.com/developer/api-docs/#operation/addShare for the response schema

        print("Created shared folder {} for {}".format(result.data.attributes.hash, folder_path))
        print("Password to access the folder is {}".format('99drowssaP?'))

    except Exception as e:
        print('Exception when calling SharesApi.addShare:', str(e))
        sys.exit(1)
