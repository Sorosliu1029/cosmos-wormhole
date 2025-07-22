from .. import entities
from .base import GetBase


class Profile(GetBase[entities.User]):
    entity_class = entities.User
    endpoint = "/v1/profile"
    get_params_key = "uid"
