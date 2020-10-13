# evapi-python

## Introduction
Welcome to ExaVault's Python code library for our v2 API. Our v2 API will allow you to interact with all aspects of the service the same way our web portal would. Included here is:
- The Python code library itself. The library is generated from our API's [public swagger YAML file](https://www.exavault.com/api/docs/evapi_2.0_public.yaml)
- Sample code showing how to use the library
- Scripts for numerous basic actions such as uploading and downloading files

## Requirements

To use this library, you'll need Python 3.x installed along with the Python package installer [pip](https://pip.pypa.io/en/stable/). 

## Installing the Code Library

### Option 0 - Using

 

### Option 1 - Using pip locally
You can use pip to add this library to your project by running this command in your project folder:

```bash
% pip install -e .
```


### Option 2 - Manual Installation
Alternatively, you can clone the [github repo](https://github.com/ExaVault/evapi-python).



## Running Your First Sample
**Step 1 - Install dependencies** 

To get started, navigate into the folder containing this code library and run pip install:

```bash 
% cd path-to-this-library
% pip install -r requirements.txt
```

This will install all the dependencies you need to run the sampples.

**Step 2 - Get your API Credentials** 

The next step is to generate an API key and token from your ExaVault account. You'll need to log into the ExaVault web file manager, as an admin-level user, to get the API key and access token. See [our API reference documentation](https://www.exavault.com/developer/api-docs/v2/#section/Obtaining-Your-API-Key-and-Access-Token) for the step-by-step guide to create your key and/or token.  

If you are not an admin-level user of an ExaVault account, you'll need someone with admin-level access to follow the steps and give you the API key and access token.

**Step 3 - Add Your API Credentials to the sample code**

Before you can make an API call, you'll need to edit the environment file provided with this code library. In that same directory where you ran `pip install -e .` above, do:

```bash
% cd samples
% cp .env.example .env
```

Edit the .env file you just created.

- replace **your\_key\_here** with your API key. Don't add any extra spaces or punctuation
- replace **your\_token\_here** with your access token.
- replace **your\_account_name** with the name of your ExaVault account

And save the file.

**Step 4 - Run the sample script**

Now you're ready to run your first sample. Try sample_get_account_info first

```bash
% python sample_get_account_info.py
```
If everything worked, the sample code will run and connect to your account. You'll see output similar to this:

```bash
% python sample_get_account_info.pys
Account used: 40GB (11.4%)
Total size: 350GB
```

**Running Other Sample Files**

There are several other sample files that you can now run. You won't need to repeat the steps to set up the .env file each time - the same environment information is used for all
of the sample scripts. Some of the sample scripts will make changes to your account (uploading, creating shares or notifications, etc). Those are marked with an asterisk below:


Script                        | Purpose    \*=Makes changes to your account when run                                   | APIs Used                      |
------------------------------|----------------------------------------------------------------------------------------|--------------------------------|
sample_add_notifications.py  | Add upload and download notifications<br/>_\*adds folders to your account_             | ResourcesApi, NotificationsApi |
sample_add_user.py           | Add a new user with a home directory <br/>_\*adds a user and a folder to your account_ | UsersApi                       |
sample_compress_files.py     | Compress several files into a zip file <br/>_\*adds files and folders to your account_ | ResourcesApi                   |
sample_download_csv_files.py | Search for files matching a certain extension, then download them.                     | ResourcesApi                   |
sample_get_account_info.py   | List the amount of available space for your account                                    | AccountApi                     |
sample_get_failed_logins.py  | List usernames who had a failed login in the last 24 hours                             | ActivityApi                    |
sample_list_users.py         | Generate a report of users in your account                                             | UsersApi                       |
sample_shared_folder.py      | Create a new shared folder with a password<br />_\*adds a folder to your account_      | ResourcesApi, SharesApi        |
sample_upload_files.py       | Upload a file to your account.<br />_\*uploads sample PDFS to your account_            | ResourcesApi                   |

## If Something Goes Wrong

**Problem - ModuleNotFoundError**

Please make sure you installed the client package (by running `pip install -e .`), and if you're trying out the sample scripts please make sure that you installed the other requirements (by running `pip install -r requirements.txt`).


**Problem - Missing the required parameter `ev_api_key`**

This error indicates there is a problem with the environment file. Make sure you have a file named .env in the same directory as the samples, and that it contains your API key, access token, and your correct account name.

**Problem - 401 Unauthorized Response**

If running the sample script returns a 401 Unauthorized error like the one shown below, there is a problem with your API credentials. Double-check that the .env file exists and contains the correct values. If all else fails, you may need to log into the ExaVault web file manager and re-issue your access token.

```bash
Exception when calling AccountApi->getAccount: [401] Client error: `GET https://exavaultsupport.exavault.com/api/v2/account` resulted in a `401 Unauthorized` response:
{"responseStatus":401,"errors":[{"code":"ERROR_INVALID_CREDENTIALS","detail":"HTTP_UNAUTHORIZED"}]}
```

**Other problems with sample code**

If you encounter any other issues running this sample code, you can contact ExaVault support for help at support@exavault.com.


## Writing Your Own Code 

When you're ready to write your own code, you can use our sample code as examples. You'll need to:

1. Download our client library 
1. Run `pip install -e` in the directory that contains our library
1. Import the library in your scripts `TODO: add package name here`
1. (Optional) You can use the .env file just like our sample scripts do.
1. Whenever you instantiate an Api object (ResourcesApi, UsersApi, etc.), override the configuration to point the code at the correct API URL:

```py
ACCOUNT_URL = "https://YOUR_ACCOUNT_NAME_HERE.exavault.com/api/v2/";
accounts_api = swagger_client.api.account_api.AccountApi()
accounts_api.api_client.configuration.host = ACCOUNT_URL
```

```py
# similar for resources_api
```
```py
# similar for users_api
```

## Author

support@exavault.com

