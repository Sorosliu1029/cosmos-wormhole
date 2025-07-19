from typing import Any

from .base import Base


class Podcast(Base):
    def __init__(
        self,
        pid: str,
        title: str,
        author: str,
        description: str,
        image: dict[str, str],
        color: dict[str, str],
        subscriptionCount: int,
        episodeCount: int,
        latestEpisodePubDate: str,
        podcasters: list[dict[str, Any]],
        **kwargs,
    ):
        super().__init__(id=pid, **kwargs)
        self.title = title
        self.author = author
        self.description = description
        self.image = image
        self.color = color
        self.subscription_count = subscriptionCount
        self.episode_count = episodeCount
        self.latest_episode_pub_date = latestEpisodePubDate
        # TODO: podcaster to user
        self.podcasters = podcasters
        # set rest keys as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f"Podcast(pid={self.id}, title={self.title})"
