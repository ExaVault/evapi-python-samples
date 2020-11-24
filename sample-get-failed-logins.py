import datetime
import os
import sys

from dotenv import load_dotenv
from exavault import ActivityApi


##
# sample_get_failed_logins.py
# Use the ActivityApi to retrieve the list of users who had failed logins in the last 24 hours.
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

    # We are demonstrating the use of the ActivityApi, which can be used to retrieve session and webhook logs
    # We have to override the default configuration of the ActivityApi object with an updated host URL so that our code
    # will reach the correct URL for the api.
    activity_api = ActivityApi()
    activity_api.api_client.configuration.host = ACCOUNT_URL

    try:
        # The getSessionLogs method of the ActivityApi class will give us access activity logs for our account
        # See https://www.exavault.com/developer/api-docs/#operation/getSessionLogs for the details of this method.

        # We must pass in our API Key and Access Token with every call, which we retrieved from the .env file above
        # This method also supports filtering parameters to limit the results returned. Check the link to
        # our API documentation for a list of those parameters.

        end_date = datetime.datetime.today()
        start_date = end_date - datetime.timedelta(days=1)

        list_result = activity_api.get_session_logs(
            API_KEY, ACCESS_TOKEN, start_date=start_date, end_date=end_date,
            type='pass', offset=0, limit=200, sort="-date"
        )

    except Exception as e:
        # If there was a problem, such as our credentials not being correct, or the URL not working,
        # there will be an exception thrown.
        print('Exception when calling ActivityApi.getSessionLogs:', str(e))
        sys.exit(1)

    # If we got this far without the program ending, our call to getSessionLogs succeeded and returned something.
    # The call returns a swagger_client.model.SessionActivityResponse object.
    # See https://www.exavault.com/developer/api-docs/#operation/getSessionLogs for the details of the response object.

    failed_logins = {}  # dictionary to hold our info

    # The returned activity will be an array of swagger_client.model.SessionActivityEntry objects, which we can access
    # from the SessionActivityResponse.data attribute.
    activity_logs = list_result.data

    # Loop over the returned items, which should include only "Connect" operations, per our 
    # filters to the get_session_logs call
    for activity in activity_logs:
        # Each SessionActivityEntry object has a getAttributes method that allows us to access the details for the
        # logged activity, which will be a swagger_client.model.SessionActivityEntryAttributes object

        # The SessionActivityEntryAttributes object has accessors for username,
        # client IP address, status, operation, etc.
        if activity.attributes.status == "failed":
            if failed_logins.get(activity.attributes.username):
                failed_logins[activity.attributes.username] += 1
            else:
                failed_logins[activity.attributes.username] = 1

    print("{} Users with failed logins:".format(len(failed_logins)))
    print("  {0: <35} {1}".format("Username", "Count"))
    print("=" * 46)

    for user, failed_count in failed_logins.items():
        print("{0: <35} {1}".format(user, failed_count))
