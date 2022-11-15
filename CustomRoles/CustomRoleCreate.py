from time import sleep
from azure.identity import ClientSecretCredential
import sys
import logging
import requests
from datetime import date
import json
import uuid

def custom_role(action, subscriptionId, role, parameter):
	client_id = ""
	# client_secret = ""
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
	print("Role Definition ID : ", role)
	print("Action : ", action)
	print("Subscription ID :", subscriptionId)
	print("Parameter :", parameter)
	if(action=='create') :
		create_custom_role = f'https://management.azure.com//subscriptions/{subscriptionId}/providers/Microsoft.Authorization/roleDefinitions/{role}?api-version=2022-04-01'
		response = requests.put(create_custom_role, headers=headers, data=parameter).json()
		print(response)
	elif(action=='update'):
		update_custom_role = f'https://management.azure.com//subscriptions/{subscriptionId}/providers/Microsoft.Authorization/roleDefinitions/{role}?api-version=2022-04-01'
		response = requests.put(update_custom_role, headers=headers, data=parameter).json()
		print(response)
	elif(action=='delete'):
		delete_role = f'https://management.azure.com//subscriptions/{subscriptionId}/providers/Microsoft.Authorization/roleDefinitions/{role}?api-version=2022-04-01'
		response = requests.delete(delete_role, headers=headers).json()
		print(response)

if __name__ == '__main__':
	subscriptionId = "40a34640-5b32-45b8-a075-2b4f82866e47"
	parameter = json.dumps({
		"properties": {
			"roleName": "SubModificationRolesss",
			"description": "SubModificationRoles",
			"type": "CustomRole",
			"permissions": [
				{
					"actions": [
						"*"
					],
					"notActions": [
						]
				}
			],
			"assignableScopes": [
				"/subscriptions/40a34640-5b32-45b8-a075-2b4f82866e47"
			]
		}
		})
	role = uuid.uuid4()
	action = "create"
	custom_role(action,subscriptionId,role, parameter)