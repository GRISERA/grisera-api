from enum import Enum


class Roles(str, Enum):
    reader = "Reader"
    editor = "Editor"
    owner = "Owner"
