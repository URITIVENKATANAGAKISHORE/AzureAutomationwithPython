from ctypes import get_last_error
from azure.identity import DefaultAzureCredential
from azure.keyvault import KeyVault
from azure.keyvault.secrets import SecretClient
import sys
import logging
import requests
from datetime import datetime, timedelta

client_id = ""
client_secret = ""
tenant_id = ""
object_id = ""

resource = 'https://management.core.windows.net/'

# Acquire a credential object using CLI-based authentication.
credential = ClientSecretCredential(
	client_id=client_id,
	client_secret=client_secret,
	tenant_id=tenant_id
)
token = credential.get_token(f'{resource}/.default')
access_token = token.token
headers = {"Authorization": 'Bearer ' + access_token, "Content-Type": 'application/json'}


subscription_Id = ""
resource_group_name = "vaultrotation"
Key_vaultName = ""




# Get the subscription information
# get_subscription = f"https://management.azure.com/subscriptions/{subscription_id}?api-version=2020-01-01"
# response = requests.get(get_subscription, headers=headers).json()

try:
    get_keyvault = f"https://management.azure.com/subscriptions/{subscription_Id}/resourceGroups/{resource_group_name}/providers/Microsoft.KeyVault/vaults/{Key_vaultName}?api-version=2022-07-01"
    response = requests.get(get_keyvault, headers=headers).json()
    if "error" in response:
        print("response: ", response)
        print("KeyVault : " + Key_vaultName + " Creatition is failed in Resource Group : " + resource_group_name)
    else:
        print("response: ", response)
        vaultBaseUrl = response["properties"]["vaultUri"]

        get_secrets = f"{vaultBaseUrl}/secrets?api-version=7.3"
        #get_secret = f"{vaultBaseUrl}/secrets/{secret_name}/{secret_version}?api-version=7.3"
        response = requests.get(get_secrets, headers=headers).json()
        if "error" in response:
            print("response: ", response)
            print("KeyVault : " + Key_vaultName + " Creatition is failed in Resource Group : " + resource_group_name)
        else:
            print("response: ", response)
            for responses in response:
                notificationDate = ( responses["attributes"]["exp"] ) - timedelta(days=30)
                if notificationDate == 60:
                    sendmail()
                    print(notificationDate)
except Exception as e:
    print(e)

