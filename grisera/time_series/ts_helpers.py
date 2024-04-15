from typing import Optional, List

from grisera.property.property_model import PropertyIn


def get_node_property(node, property_key: str):
    if node is not None:
        for node_property in node["properties"]:
            if node_property["key"] == property_key:
                return node_property["value"]
    return None


def get_additional_parameter(additional_properties: Optional[List[PropertyIn]], key: str):
    if additional_properties is not None:
        for additional_property in additional_properties:
            if additional_property.key == key:
                return additional_property.value
    return None
