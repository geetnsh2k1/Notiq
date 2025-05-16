from enum import Enum


class RedirectionType(str, Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
