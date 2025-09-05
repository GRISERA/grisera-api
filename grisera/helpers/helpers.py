import requests
from fastapi import Request, Depends, HTTPException
from typing import Union

from grisera.auth.auth_bearer import JWTBearer
from grisera.auth.auth_module import Roles

from grisera.auth.auth_config import PERMISSIONS_ENDPOINT, KEYCLOAK_SERVER, REALM, CLIENT_ID, CLIENT_SECRET


def create_stub_from_response(response, id_key='id', properties=None):
    if properties is None:
        properties = []
    stub = {id_key: response['id'], 'additional_properties': []}

    if 'properties' in response and response["properties"] is not None:
        for prop in response["properties"]:
            if properties is not None and 'key' in prop and prop['key'] in properties:
                stub[prop['key']] = prop['value'] if 'value' in prop else None
            else:
                stub['additional_properties'].append({'key': prop['key'], 'value': prop['value']})

    return stub


def check_dataset_permission(request: Request, dataset_id: Union[int, str], token=Depends(JWTBearer())):
    user_id = token['sub']
    permissions = get_permissions(user_id)
    for permission in permissions:
        if str(permission['datasetId']) == str(dataset_id):
            if (not request.method == "GET") and (str(permission['role']) == Roles.reader):
                raise HTTPException(status_code=403, detail="Invalid permission level to dataset")
            return dataset_id

    raise HTTPException(status_code=403, detail="Invalid authentication to dataset")


def get_permissions(user_id: Union[int, str]):
    access_token = _getAccessToken()
    return _request_permissions(access_token, user_id)


def _getAccessToken():
    url = f"{KEYCLOAK_SERVER}/realms/{REALM}/protocol/openid-connect/token"

    payload = f'grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"Token request failure: {response.status_code}, {response.json()}")
        raise http_err

    return response.json()['access_token']


def _request_permissions(access_token, user_id):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(f'{PERMISSIONS_ENDPOINT}/{user_id}', headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        response = http_err.response
        print(f"Request failure: {response.status_code}, {response.json()}")
        return response.json()
