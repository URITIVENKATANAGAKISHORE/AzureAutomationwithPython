from ctypes import get_last_error
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import sys
import logging
import requests
from datetime import date

client_id = "a19cdd4e-e230-49e3-9244-e66ddc0ff0cd"
client_secret = "xLW8Q~XcR9kQbKCDsRkAU9zoaGniSTJcKWPqjcu2"
tenant_id = "25601436-dd8f-46c2-8c62-8db59303315f"
object_id = "313824b9-6ea5-4967-92c6-bff2cd42f818"

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


subscription_id = ""
resource_groupname = "vaultrotation"
Key_vaultName = ""

# Get the subscription information
# get_subscription = f"https://management.azure.com/subscriptions/{subscription_id}?api-version=2020-01-01"
# response = requests.get(get_subscription, headers=headers).json()


get_keyvault = f"https://management.azure.com/subscriptions/{subscription_Id}/resourceGroups/{resource_groupname}/providers/Microsoft.KeyVault/vaults/{Key_vaultName}?api-version=2022-07-01"
response = requests.get(get_keyvault, headers=headers).json()

vaultBaseUrl = response.vaultUri 

get_secrets = f"{vaultBaseUrl}/secrets?api-version=7.3"
#get_secret = f"{vaultBaseUrl}/secrets/{secret_name}/{secret_version}?api-version=7.3"

response = requests.get(get_secrets, headers=headers).json()
response.created
response.exp

get_storageKeys = f"https://management.azure.com/subscriptions/{subscription_Id}/resourceGroups/{resource_groupname}/providers/Microsoft.Storage/storageAccounts/{storage_accountName}/listKeys?api-version=2022-05-01"
response = requests.get(get_storageKeys, headers=headers).json()


for keyName in response.keys.keyName :
    
    create_secret =  f"{vaultBaseUrl}/secrets/{secret_name}?api-version=7.3"
    data = json.dumps({
        "value": "mysecretvalue"
    })
    response = requests.put(create_secret, headers=headers, data=data).json()   