from azure.identity import ClientSecretCredential
import sys
import logging
import requests
from datetime import date,datetime
import calendar


client_id = "a1e91c47-7395-4d0d-9848-b8a8701cd9ca"
#client_secret = "vPV8Q~rR2BxDA8J2suhSOqBioKESj7Fy6wUgxaSp"
client_secret = "Rgq8Q~MP~iwKdUtZzkndb2TDuZVl2yDb_C0X5bIN"
tenant_id = "9df8e718-be03-4924-b844-0eb5c254f63e"
object_id = "ec24629d-9352-4668-841d-a29d14ad4bb0"

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

subscriptionId = "40a34640-5b32-45b8-a075-2b4f82866e47"
resourceGroupName = "vaultrotation"
storageAccountName = "vaultrotationstorage43"
keyVaultName = "vaultrotation-kv43"
try :


	get_resourcegroupname = f"https://management.azure.com/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}?api-version=2021-04-01"
	response = requests.get(get_resourcegroupname, headers=headers).json()
	#print(response)

	resourceGroupName = response['name']
	location = response['location']
	print("Resource Group Name : ", resourceGroupName)
	print("Location : ", location)

	get_storageaccountname = f'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{storageAccountName}?api-version=2022-05-01'
	response = requests.get(get_storageaccountname, headers=headers).json()
	#print(response)
	storageAccountName = response['name']
	print("Storage Account Name : ", storageAccountName)

	get_storageaccount_keys = f'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{storageAccountName}/listKeys?api-version=2022-05-01'
	response = requests.get(get_storageaccount_keys, headers=headers).json()
	print(response)
	"""for item in response['keys']:
		if item.keyName == 'key1':
			print("Key1: ", item.value)
		if item.keyName == 'key2':
			print("Key2: ", item.value)
	"""
	get_keyvault = f'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.KeyVault/vaults/{keyVaultName}?api-version=2022-07-01'
	response = requests.get(get_keyvault, headers=headers).json()
	#print(response)
	keyVaultName = response['name']
	vaultBaseUrl = response['properties']['vaultUri']
	print("Keyvault Account Name : ", keyVaultName)
	print("Vault URI : ", vaultBaseUrl)

	get_role = f'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/roleAssignments?api-version=2022-04-01&$filter=atScope()'
	response = requests.get(get_role, headers=headers).json()
	print(response)

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

	currentdate = datetime.now()
	isttimestamp = int(currentdate.timestamp())
	print("IST TIME :", isttimestamp)

	get_secret_list = f'{vaultBaseUrl}/secrets?api-version=7.3'
	response = requests.get(get_secret_list, headers=headers).json()
	#print(response)
	for item in response['value']:
		keyvalue = item['contentType']
		if keyvalue == 'key1':
			id = item['id']
			nbf = item['attributes']['nbf']
			exp = item['attributes']['exp']
			created = item['attributes']['created']
			difference =  item['attributes']['exp'] - 172800
			print("keyValue : ", keyvalue)
			print("ID : ", id)
			print("NBF : ", nbf)
			print("EXP : ", exp)
			print("Created : ", created)
			print("Difference : ", difference)
		if keyvalue == 'key2':
			id = item['id']
			nbf = item['attributes']['nbf']
			exp = item['attributes']['exp']
			created = item['attributes']['created']
			difference =  item['attributes']['exp'] - 172800
			print("keyValue : ", keyvalue)
			print("ID : ", id)
			print("NBF : ", nbf)
			print("EXP : ", exp)
			print("Created : ", created)
			print("Difference : ", difference)


	#get_secret_version = f'{vaultBaseUrl}/secrets/{storageAccountNamekey}/versions?api-version=7.3'
	#response = requests.get(get_secret_version, headers=headers).json()

	#put_secret_list = f''

except Exception as e :
	print()