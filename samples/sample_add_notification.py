import datetime
import os
import sys

from dotenv import load_dotenv
from swagger_client.api.resources_api import ResourcesApi
from swagger_client.api.notifications_api import NotificationsApi

##
# sample_get_notification.py
# Use the NotificationsApi to create a Notification on a folder
##

# To use this script, add your credentials to a file named .env which is located in the same directory as the script
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

load_dotenv()
API_KEY = os.getenv('EV_KEY')
ACCESS_TOKEN = os.getenv('EV_TOKEN')
ACCOUNT_URL = os.getenv('ACCOUNT_URL')


if __name__ == "__main__":
    # We are demonstrating the use of the NotificationsApi, which can be used to manage notification settings
    # for files and folders.
    #
    # For this demo, we'll create a new folder tree and add notifications to those new folders. If you have
    # an existing file or folder that you want to create a notification for, you won't need the step where
    # we use the ResourcesApi to create the folders first.
    #
    # We have to override the default configuration of the API object with an updated host URL so that our code
    # will reach the correct URL for the api. We have to override this setting for each of the API classes we use.

    resources_api = ResourcesApi()
    resources_api.api_client.configuration.host = ACCOUNT_URL

    try:
        # We will create a new folder tree for the demo. The top-level folder will
        # have a different name each time you run this script
        parent_folder = "sample_notifications_{}".format(datetime.datetime.today().strftime("%s"))

        # We can actually be sneaky and add missing parent folders by passing a multi-level path
        upload_folder = "/{}/uploads".format(parent_folder)
        download_folder = "/{}/downloads".format(parent_folder)

        # API methods that take a JSON body, such as the add_folder method, require us to submit a dictionary with the
        # parameters we want to send to the API. This call requires a single parameter path
        request_body = {
            'path': upload_folder
        }

        # We have to pass the API_KEY and ACCESS_TOKEN with every API call.
        result = resources_api.add_folder(API_KEY, ACCESS_TOKEN, body=request_body)

        # The add_folder method of the ResourcesApi returns a swagger_client.model.ResourceResponse object
        # See https://www.exavault.com/developer/api-docs/#operation/addFolder for
        # the details of the response object

        print("Created new folder {}".format(result.data.attributes.path))

        # Now we can add the second folder
        request_body = {'path': download_folder}
        result = resources_api.add_folder(API_KEY, ACCESS_TOKEN, body=request_body)

        # The add_folder method of the ResourcesApi returns a swagger_client.model.ResourceResponse object
        # See https://www.exavault.com/developer/api-docs/#operation/addFolder for the details of the
        # response object
        print("Created new folder {}".format(result.data.attributes.path))

    except Exception as e:
        print('Exception when calling resources_api.add_folder: ', str(e))
        sys.exit(1)

    # If we got this far without the program ending, we were able to set up our folders to create 
    # notifications, and now we can use the NotificationsApi to create those.
    # We have to override the default configuration of the API object with an updated host URL so that 
    # our code will reach the correct URL for the api.

    notifications_api = NotificationsApi()
    notifications_api.api_client.configuration.host = ACCOUNT_URL

    try:
        # API methods that take a JSON body, such as the add_folder method, require us to submit an object with the
        # parameters we want to send to the API.
        # See https://www.exavault.com/developer/api-docs/#operation/addNotification for the request body schema
        # - We want to be notified by email whenever anyone downloads from our downloads folder, so we are using
        #   the constant "notice_user_all", which means anyone, including users and share recipients.
        #   See  https://www.exavault.com/developer/api-docs/#operation/addNotification  for a list of other
        #   constants that can be used in the usernames array
        # - Note that the download_folder variable contains the full path to the folder that was created earlier
        # - We could also have pulled the ID for the new folder out of the ResourceResponse object and used that
        #   as a resource identifier here. For example, if the ID of the downloads folder is 23422, we could pass
        #   id:23422 in the resource parameter of this call.
        request_body = {
            'type': 'folder',
            'resource': download_folder,
            'action': 'download',
            'usernames': ['notice_user_all'],
            'sendEmail': True
        }

        # We have to pass the API_KEY and ACCESS_TOKEN with every API call.
        result = notifications_api.add_notification(API_KEY, ACCESS_TOKEN, body=request_body)
        print("Created download notification for {}".format(download_folder))

        # - Next we will add a notification that will send a message to several addresses when a user uploads
        #   into our uploads folder.
        # - As with the other notification, we will pass in the full path to the folder in the resource parameter
        #
        # There are some things we're doing differently:
        #   - We're using a different constant for the usernames parameter "notice_users_all_users", which means
        #   only trigger notifications when an action is done by a user account (not share recipients)
        #   See  https://www.exavault.com/developer/api-docs/#operation/addNotification for a list of other
        #   constants that can be used in the usernames array
        #   - We are sending the notification to a bunch of email addresses, rather than just our own
        #   - We have added an optional custom message to be included in each notification email
        request_body = {
            'type': 'folder',
            'resource': upload_folder,
            'action': 'upload',
            'usernames': ['notice_user_all_users'],
            'sendEmail': True,
            'recipients': [
                'sally@example.com',
                'sidharth@example.com',
                'lgomez@example.com'
            ],
            'message': 'Files have been uploaded into the main folder for you.'
        }

        # We have to pass the API_KEY and ACCESS_TOKEN with every API call.
        result = notifications_api.add_notification(API_KEY, ACCESS_TOKEN, body=request_body)
        print("Created upload notification for {}".format(upload_folder))

    except Exception as e:
        print('Exception when calling NotificationsApi.add_notification:', str(e))
        sys.exit(1)
