import json
import requests

from azure.identity import ClientSecretCredential

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

# list of subscriptions
get_subscription_list = f"https://management.azure.com/subscriptions?api-version=2020-01-01"
response = requests.get(get_subscription_list, headers=headers).json()
print(response)

subscription_id = "40a34640-5b32-45b8-a075-2b4f82866e47"
get_subscription = f"https://management.azure.com/subscriptions/{subscription_id}?api-version=2020-01-01"
response = requests.get(get_subscription, headers=headers).json()
print(response)

id = response['id']
subscription_id = response['subscriptionId']
tenant_id = response['tenantId']
subscription_name = response['displayName']
subscription_name_alias = (subscription_name[0:5] + "testing").lower()
status = response['state']
location = "eastus"
resource_group_name = subscription_name_alias + "-" + location + "-app-rg"
storage_account_name = subscription_name_alias + location + "sa"
key_vault_name = subscription_name_alias + location + "kv"
userassigned_identiy_name = "azzuretesting--usmi"

print("ID : ", id)
print("Subscription ID : ", subscription_id)
print("Tenant ID : ", tenant_id, )
print("Object ID:", object_id)
print("Subscription Name : ", subscription_name)
print("Subscription Alias Name : ", subscription_name_alias)
print("Status : ", status)
print("Location : ", location)
print("Resource Group Name : ", resource_group_name)
print("Storage Account Name : ", storage_account_name)
print("Key Vault Name : ", key_vault_name)

