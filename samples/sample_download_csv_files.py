import datetime
import os
import sys

from dotenv import load_dotenv
from swagger_client.api.resources_api import ResourcesApi

# TODO: download_api not found

##
# sample_download_csv_files.py - Use the ResourcesApi to download all of the CSV files found within a folder tree
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

    # We have to override the default configuration of the API object with an updated host URL so that our code
    # will reach the correct URL for the api. We have to override this setting
    # for each of the API classes we use
    resources_api = ResourcesApi()
    resources_api.api_client.configuration.host = ACCOUNT_URL

    try:
        # For this demo, we want to download all of the CSV files located within a certain folder.
        # - Your account comes pre-loaded with a folder tree named "Sample Files and Folders" which contains
        # a folder tree containing many samples. If you have renamed, deleted or moved this folder,
        # this demo script will not work.

        # First, we'll get a list of all the CSV files within the desired folder

        list_result = resources_api.list_resources(
            API_KEY, ACCESS_TOKEN, "/Sample Files and Folders", offset=0, type='file', name='*.csv')

        # The ResourcesApi::listResources method returns a .Swagger.Client.Model.ResourceCollectionResponse object
        # See https://www.exavault.com/developer/api-docs/#operation/listResources for the response schema

        # The ResourceCollectionResponse::getReturnedResults method will indicate how many matching files are included
        # in this response. If we didn't find any matches, there's nothing else to do
        if list_result.returned_results == 0:
            print("Found no files to download")
            sys.exit(0)
        else:
            print("Found {} CSV files to download".format(list_result.returned_results))

    except Exception as e:
        print('Exception when calling Api:', str(e))
        sys.exit(1)

    # If we got this far, there are files for us to download
    # We are going to save the IDs of all the files we want to download into an array
    downloads = []
    listed_files = list_result.data
    for listed_file in listed_files:
        downloads.append("id:{}".format(listed_file.id))
        print(listed_file.attributes.path)

    try:
        # Now that we used the ResourcesApi to gather all of the IDs of the resources that
        # matched our search, we will use the DownloadApi to download multiple files
        ##*************************************************************************************##
        ## note - this is an unusual workaround required by the auto-generated py cl_ient sdk *##
        ##*************************************************************************************##
        # ideally, we would use the resources_api for all resources calls, but due to a bug in
        # the library that creates the ResourcesApi, you cannot download multiple files at once
        # using that API. Instead, use the DownloadApi download methods which has the same parameters and
        # output as the ResourcesApi See https://www.exavault.com/developer/api-docs/#operation/download
        ##
        ##*********************************************************************************##

        # TODO: Looks like this API is returning non-ASCII response
        result = resources_api.download(API_KEY, ACCESS_TOKEN, downloads)

        # The body of the result is the binary content of our file(s),
        # We write that content into a single file, named with .zip if there were multiple files
        # downloaded or just named .csv if not (since we were storing csvs)
        if len(downloads) > 1:
            download_file = os.path.join(os.path.dirname(__file__), "files/download.zip")
        else:
            download_file = os.path.join(os.path.dirname(__file__),
                                         "files/download-{}.csv".format(datetime.datetime.today().strftime("%s")))

        with open(download_file, 'w') as f:
            f.write(result)

        print("File(s) downloaded to", download_file)

    except Exception as e:
        raise e
        print('Exception when calling Api:', str(e))
        sys.exit(1)
