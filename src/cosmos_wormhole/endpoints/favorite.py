from .. import entities
from .base import ListBase


class FavoritedEpisode(ListBase[entities.Episode]):
    entity_class = entities.Episode
    endpoint = "/v1/favorite"


class FavoritedComment(ListBase[entities.Comment]):
    entity_class = entities.Comment
    endpoint = "/v1/comment/collect"
