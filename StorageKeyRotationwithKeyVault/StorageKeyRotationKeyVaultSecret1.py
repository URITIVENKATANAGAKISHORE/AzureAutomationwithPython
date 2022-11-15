from azure.identity import ClientSecretCredential
import sys
import logging
import requests
from datetime import date

client_id = "a1e91c47-7395-4d0d-9848-b8a8701cd9ca"
#client_secret = "vPV8Q~rR2BxDA8J2suhSOqBioKESj7Fy6wUgxaSp"
client_secret = "Rgq8Q~MP~iwKdUtZzkndb2TDuZVl2yDb_C0X5bIN"
tenant_id = "9df8e718-be03-4924-b844-0eb5c254f63e"
object_id = "ec24629d-9352-4668-841d-a29d14ad4bb0"

resource = 'https://vault.azure.net'

# Acquire a credential object using CLI-based authentication.
credential = ClientSecretCredential(
	client_id=client_id,
	client_secret=client_secret,
	tenant_id=tenant_id
)
token = credential.get_token(f'{resource}/.default')
access_token = token.token
headers = {"Authorization": 'Bearer ' + access_token, "Content-Type": 'application/json'}

subscriptionId = "40a34640-5b32-45b8-a075-2b4f82866e47"
resourceGroupName = "vaultrotation"
storageAccountName = "vaultrotationstorage43"
keyVaultName = "vaultrotation-kv43"
vaultBaseUrl = "https://vaultrotation-kv43.vault.azure.net/"
try :

	get_keyvault_keys = f'{vaultBaseUrl}/secrets?api-version=7.3'
	response = requests.get(get_keyvault_keys, headers=headers).json()
	print(response)
	if "error" in response:
		print("Error")
	else :
		print(response)
	#put_secret = f'{vaultBaseUrl}/secrets/{secret-name}?api-version=7.3'
	#data =
	#response = requests.put(put_secret, headers=headers, data=data).json()
	#print(response)
	#{
	#	"value": "mysecretvalue"
	#}
except Exception as e :
	print()