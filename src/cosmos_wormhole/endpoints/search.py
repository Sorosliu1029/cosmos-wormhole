from typing import AsyncGenerator

import entities

from .base import ListBase


class PodcastSearch(ListBase[entities.Podcast]):
    entity_class = entities.Podcast
    endpoint = "/v1/search"
    list_suffix = "create"
    list_body = {"limit": 20}

    def search(self, keyword: str) -> AsyncGenerator[entities.Podcast, None]:
        return self.list({"keyword": keyword, "type": "PODCAST"})


class EpisodeSearch(ListBase[entities.Episode]):
    entity_class = entities.Episode
    endpoint = "/v1/search"
    list_suffix = "create"
    list_body = {"limit": 20}

    def search(self, keyword: str) -> AsyncGenerator[entities.Episode, None]:
        return self.list({"keyword": keyword, "type": "EPISODE"})


class UserSearch(ListBase[entities.User]):
    entity_class = entities.User
    endpoint = "/v1/search"
    list_suffix = "create"
    list_body = {"limit": 20}

    def search(self, keyword: str) -> AsyncGenerator[entities.User, None]:
        return self.list({"keyword": keyword, "type": "USER"})
