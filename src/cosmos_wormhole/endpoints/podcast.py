from .. import entities
from .base import GetBase


class Podcast(GetBase[entities.Podcast]):
    entity_class = entities.Podcast
    endpoint = "/v1/podcast"
    get_params_key = "pid"
