import os
import sys

from dotenv import load_dotenv
from exavault import UsersApi

##
# sample_list_users.py - Use the UsersApi to create a report of account users
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

    # We are demonstrating the use of the UsersApi, which can be used to retrieve user settings and create a report
    # We have to override the default configuration of the UserApi object with an updated host URL so that our code
    #  will reach the correct URL for the api.
    users_api = UsersApi()
    users_api.api_client.configuration.host = ACCOUNT_URL

    # List to store our results in
    list_of_users = []

    try:
        # The listUsers method of the UsersApi class will give us access the users defined in our account
        # See https://www.exavault.com/developer/api-docs/#operation/listUsers for the details of this method

        # We must pass in our API Key and Access Token with every call, which we retrieved from the .env file above
        # This method also supports filtering parameters to limit the results returned. Check the link to
        # our API documentation for a list of those parameters.
        list_result = users_api.list_users(API_KEY, ACCESS_TOKEN)

    except Exception as e:

        # If there was a problem, such as our credentials not being correct, or the URL not working,
        # there will be an exception thrown.
        print('Exception when calling UserApi.listUsers:', str(e))
        sys.exit(1)

    # If we got this far without the program ending, our call to list_users succeeded and returned something
    # The call returns a swagger_client.model.UserCollectionResponse object
    # See https://www.exavault.com/developer/api-docs/#operation/listUsers for
    # the details of the response object

    total_users_for_account = list_result.total_results
    total_users_retrieved = list_result.returned_results

    # The returned users will be an array of wagger_client.model.User objects which we can access from the
    # UserCollectionResponse.data attribute
    users_retrieved = list_result.data

    # We are creating a CSV file in the same directory as this script.
    #
    # This opens the file for writing (which removes existing data) and gives us a file handle that we
    # can use to write the CSV data with.
    output_filename = os.path.join(os.path.dirname(__file__), "files/users_listing.csv")
    with open(output_filename, 'w') as f:

        # Writing the column titles to our CSV file
        csv_column_headers = [
            'Id',
            'Username',
            'Nickname',
            'Email Address',
            'Home Folder',
            'Role',
            'Time Zone',
            'Download',
            'Upload',
            'Modify',
            'Delete',
            'List',
            'Change Password',
            'Share',
            'Notification',
            'View Form Data',
            'Delete Form Data',
            'Expiration',
            'Last Logged In',
            'locked',
            'Created',
            'Modified']
        f.write(','.join(csv_column_headers) + '\n')

        # Looping over the users array that we got back from our list_users call.
        for user in users_retrieved:

            # The internal ID of a user isn't visible in the web file manager. It is used by the API to
            # access the user.
            user_id = user.id

            # The detailed data about the individual user is accessed through the User.attributes attribute
            # which returns a swagger_client.model.UserAttributes object

            username = user.attributes.username
            nickname = user.attributes.nickname
            email = user.attributes.email
            home_dir = user.attributes.home_dir
            role = user.attributes.role
            time_zone = user.attributes.time_zone
            created = user.attributes.created
            modified = user.attributes.modified
            access_timestamp = user.attributes.access_timestamp
            expiration = user.attributes.expiration if user.attributes.expiration else ''
            locked = '' if user.attributes.status else 'locked'

            # The access timestamp returns a non-standard value representing 'never'
            last_logged_in = 'never' if access_timestamp[:4] == "0000" else access_timestamp

            # The UserAttributes.permissions attribute returns a swagger_client.model.UserPermissions object,
            #   which contains the True/False flags for each of the permissions available to a user
            #   See https://www.exavault.com/docs/account/04-users/00-introduction#managing-user-roles-and-permissions
            #
            download = 'download' if user.attributes.permissions.download else ''
            upload = 'upload' if user.attributes.permissions.upload else ''
            modify = 'modify' if user.attributes.permissions.modify else ''
            delete = 'delete' if user.attributes.permissions.delete else ''
            list_permission = 'list' if user.attributes.permissions.list else ''
            change_password = 'change_password' if user.attributes.permissions.change_password else ''
            share = 'share' if user.attributes.permissions.share else ''
            notification = 'notification' if user.attributes.permissions.notification else ''
            view_form_data = 'view_form_data' if user.attributes.permissions.view_form_data else ''
            delete_form_data = 'delete_form_data' if user.attributes.permissions.delete_form_data else ''

            # Make an array of the current user's data and append it to the list we
            # will use to create our report
            data = [
                user_id,
                username,
                nickname,
                email,
                home_dir,
                role,
                time_zone,
                download,
                upload,
                modify,
                delete,
                list_permission,
                change_password,
                share,
                notification,
                view_form_data,
                delete_form_data,
                expiration,
                last_logged_in,
                locked,
                created,
                modified]
            f.write(','.join(map(str, data)) + '\n')

    print("Listed: {} users to {}".format(total_users_retrieved, output_filename))
