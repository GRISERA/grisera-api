def create_stub_from_response(response, id_key='id', properties=[]):
    stub = {id_key: response['id'], 'additional_properties': []}

    if 'properties' in response and response["properties"] is not None:
        for prop in response["properties"]:
            if properties is not None and 'key' in prop and prop['key'] in properties:
                stub[prop['key']] = prop['value'] if 'value' in prop else None
            else:
                stub['additional_properties'].append({'key': prop['key'], 'value': prop['value']})

    return stub
