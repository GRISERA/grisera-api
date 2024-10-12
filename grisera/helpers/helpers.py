from fastapi import Request, Depends, HTTPException
from typing import Union

from grisera.auth.auth_bearer import JWTBearer
from grisera.auth.auth_module import Roles


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
    for permission in token['permissions']:
        if str(permission['datasetId']) == str(dataset_id):
            if (not request.method == "GET") and (str(permission['role']) == Roles.reader):
                raise HTTPException(status_code=403, detail="Invalid permission level to dataset")
            return dataset_id

    raise HTTPException(status_code=403, detail="Invalid authentication to dataset")
