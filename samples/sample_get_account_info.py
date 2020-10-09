from __future__ import division
import os
import sys

# The following line is required because the swagger_client is in the sibling directory.
# We may remove the line if we choose to put it inside the samples directory.
# Also, we may not need it if we directly publish the client to pypi and use that instead.
sys.path.append(os.path.abspath('../'))

from dotenv import load_dotenv
from swagger_client.api.account_api import AccountApi

##
# sample_get_account.py
# Use the AccountApi to return your account info and check disk usage
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
    # We are demonstrating the use of the AccountAPI, which can be used to manage the account settings
    # We have to override the default configuration of the AccountApi with an updated host URL so that our code
    # will reach the correct URL for the api.
    api = AccountApi()
    api.api_client.configuration.host = ACCOUNT_URL

    result = None
    try:
        # The getAccount method of the AccountApi class will give us access to the current status of our account
        # See https://www.exavault.com/developer/api-docs/#operation/getAccount for the details of this method
        # We must pass in our API Key and Access Token with every call, which we retrieved from the .env file above
        result = api.get_account(API_KEY, ACCESS_TOKEN)
    except Exception as e:
        # If there was a problem, such as our credentials not being correct, or the URL not working,
        # there will be an exception thrown
        print('Exception when calling AccountApi.get_account: ', str(e))
        sys.exit(1)

    # If we got this far without the program ending, our call to getAccount succeeded and returned something
    # The call returns a `swagger_client.models.account_response.AccountResponse` object
    # See https://www.exavault.com/developer/api-docs/#operation/getAccount for the details of the response object
    #
    # The AccountResponse object that we got back (`result`) is composed of additional, nested objects
    # The Quota object will tell us how much space we've used
    quota = result.data.attributes.quota
    account_max_size = quota.disk_limit / (1024 ** 3)
    account_current_size = quota.disk_used / (1024 ** 3)

    print('Account used: {:.1f} GB ({:.1f}%)'.format(
        account_current_size, account_current_size/account_max_size * 100))
    print('Total size: {:.1f} GB'.format(account_max_size))
