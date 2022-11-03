import json
import requests

from azure.identity import ClientSecretCredential

client_id = "a19cdd4e-e230-49e3-9244-e66ddc0ff0cd"
client_secret = "xLW8Q~XcR9kQbKCDsRkAU9zoaGniSTJcKWPqjcu2"
tenant_id = "25601436-dd8f-46c2-8c62-8db59303315f"
object_id = "313824b9-6ea5-4967-92c6-bff2cd42f818"
#principal_id = ""

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

subscription_id = "175ca0e1-3559-4ca6-96aa-1027844d3d64"
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


def create_update_resource_group(**kwargs):
	try:
		#
		get_resource_group_name = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{resource_group_name}?api-version=2021-04-01"
		response = requests.get(get_resource_group_name, headers=headers).json()
		print(response)
		# scope = response['id']

		if "error" in response:
			print("Resource Group : " + resource_group_name + " is not created")
			print("Beggining the Resource Group Creation")
			create_resource_group_name = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{resource_group_name}?api-version=2021-04-01"
			data = json.dumps({
				"location": location
			})
			response = requests.put(create_resource_group_name, headers=headers, data=data).json()
			print("response: ", response)
			print("Resource Group : " + resource_group_name + " is  created")
			print("Resource Group ID : " + response['id'])
			scope = response['id']
		else:
			print("Resource Group : " + resource_group_name + " is already created")
	except Exception as e:
		print(e)


def provider_registration(**kwargs):
	try:
		#
		service = ['Microsoft.Storage', 'Microsoft.KeyVault', 'Microsoft.EventGrid', 'Microsoft.ManagedIdentity',
				   'Microsoft.Web', 'Microsoft.Sql', 'Microsoft.Network', 'Microsoft.OperationalInsights',
				   'Microsoft.Compute', 'Microsoft.Authorization']
		# [' Microsoft.Maintenance ',' Microsoft.Logic ',' Microsoft.Cdn ',' Microsoft.ServiceFabric ',' Microsoft.Automation ',' Microsoft.EventHub ',' Microsoft.PowerBIDedicated ',' Microsoft.Kusto ',' Microsoft.ServiceFabricMesh ',' microsoft.insights ',' Microsoft.Compute ',' Microsoft.OperationalInsights ',' Microsoft.KeyVault ',' Microsoft.Cache ',' Microsoft.ContainerInstance ',' Microsoft.TimeSeriesInsights ',' Microsoft.DBforPostgreSQL ',' Microsoft.Media ',' Microsoft.HDInsight ',' Microsoft.Search ',' Microsoft.DevTestLab ',' Microsoft.Databricks ',' Microsoft.OperationsManagement ',' Microsoft.Devices ',' Microsoft.CustomProviders ',' Microsoft.SecurityInsights ',' Microsoft.ServiceBus ',' Microsoft.MachineLearningServices ',' Microsoft.Relay ',' Microsoft.Sql ',' Microsoft.DBforMariaDB ',' Microsoft.CognitiveServices ',' Microsoft.ContainerService ',' Microsoft.ManagedIdentity ',' Microsoft.DataMigration ',' Microsoft.RecoveryServices ',' Microsoft.NotificationHubs ',' Microsoft.AppPlatform ',' Microsoft.DocumentDB ',' Microsoft.MixedReality ',' Microsoft.DataLakeStore ',' Microsoft.Storage ',' Microsoft.EventGrid ',' Microsoft.DesktopVirtualization ',' Microsoft.BotService ',' Microsoft.Maps ',' Microsoft.StreamAnalytics ',' Microsoft.DevSpaces ',' Microsoft.DBforMySQL ',' Microsoft.DataLakeAnalytics ']
		for service_name in service:

			get_service_name = f"https://management.azure.com/subscriptions/{subscription_id}/providers/{service_name}/register?api-version=2021-04-01"
			response = requests.get(get_service_name, headers=headers).json()
			if "error" in response:
				create_service_name = f"https://management.azure.com/subscriptions/{subscription_id}/providers/{service_name}/register?api-version=2021-04-01"
				response = requests.put(create_service_name, headers=headers).json()
				print("Service Name : " + service_name + " is Registered")
			else:
				print("Service Name : " + service_name + " is Already Registered")

	except Exception as e:
		print(e)


def create_update_storage_account(**kwargs):
	try:
		#
		get_storage_account_name = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}?api-version=2021-09-01"
		response = requests.get(get_storage_account_name, headers=headers).json()
		if "error" in response:
			print(
				"Storage Account : " + storage_account_name + " is not Create in Resource Group : " + resource_group_name)
			print("Beggining the Storage Account Creation")
			create_storage_account = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}?api-version=2021-09-01"
			data = json.dumps({
				"sku": {
					"name": "Premium_LRS"
				},
				"kind": "BlockBlobStorage",
				"location": location
			})
			response = requests.put(create_storage_account, headers=headers, data=data).json()
			print(response)
			if "error" in response:
				print("response: ", response)
				print(
					"Storage Account : " + storage_account_name + " Creatition is failed in Resource Group : " + resource_group_name)
			else:
				print("response: ", response)
				print(
					"Storage Account : " + storage_account_name + " is Created in Resource Group : " + resource_group_name)
		else:
			print(
				"Storage Account : " + storage_account_name + " is Already Created in Resource Group : " + resource_group_name)
	except Exception as e:
		print(e)


def Get_managed_identity():
	try:
		get_storage_account_name = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}?api-version=2021-09-01"
		response = requests.get(get_storage_account_name, headers=headers).json()
		print(response)
		print("ID : " + response['id'])
		print("Storage Name : " + response['name'])

		get_managed_identiy = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{userassigned_identiy_name}?api-version=2018-11-30"
		response = requests.get(get_managed_identiy, headers=headers).json()
		print(response)

		f"POST https://myvault.vault.azure.net//keys/Key01/rotate?api-version=7.3"
	except Exception as e:
		print(e)
