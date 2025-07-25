from datetime import datetime
from typing import Any, Literal

from .base import Base
from .user import User


class Podcast(Base):
    def __init__(
        self,
        pid: str,
        title: str,
        author: str = "",
        description: str = "",
        brief: str = "",
        image: dict[str, str] = {},
        color: dict[str, str] = {},
        subscriptionCount: int = 0,
        episodeCount: int = 0,
        latestEpisodePubDate: str = "",
        podcasters: list[dict[str, Any]] = [],
        subscritionStatus: Literal["ON", "OFF"] = "OFF",
        **kwargs,
    ):
        super().__init__(id=pid)
        self.title = title
        self.author = author
        self.description = description
        self.brief = brief
        self.image = image
        self.color = color
        self.subscription_count = subscriptionCount
        self.episode_count = episodeCount
        self.latest_episode_pub_date = (
            datetime.fromisoformat(latestEpisodePubDate)
            if latestEpisodePubDate
            else None
        )
        self.podcasters = [
            User(**podcaster) if isinstance(podcaster, dict) else podcaster
            for podcaster in podcasters
        ]
        self.subscription_status = subscritionStatus
        # set rest keys as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f"Podcast(pid={self.id}, title={self.title})"
