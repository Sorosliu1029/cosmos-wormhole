from typing import Any

import entities

from .base import ListBase


class FavoritedEpisode(ListBase[entities.Episode]):
    entity_class = entities.Episode
    endpoint = "/v1/favorite"
