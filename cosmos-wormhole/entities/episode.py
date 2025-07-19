from datetime import datetime
from typing import Any

from .base import Base
from .podcast import Podcast


class Episode(Base):
    def __init__(
        self,
        eid: str,
        pid: str,
        title: str,
        description: str = "",
        shownotes: str = "",
        duration: int = 0,
        image: dict[str, Any] = {},
        enclosure: dict[str, str] = {},
        mediaKey: str = "",
        media: dict[str, Any] = {},
        playCount: int = 0,
        playTime: int = 0,
        clapCount: int = 0,
        commentCount: int = 0,
        favoriteCount: int = 0,
        pubDate: str = "",
        podcast: dict = {},
        **kwargs,
    ):
        super().__init__(id=eid)
        self.pid = pid
        self.title = title
        self.description = description
        self.shownotes = shownotes
        self.duration = duration
        self.image = image
        self.enclosure = enclosure
        self.media_key = mediaKey
        self.media = media
        self.play_count = playCount
        self.play_time = playTime
        self.clap_count = clapCount
        self.comment_count = commentCount
        self.favorite_count = favoriteCount
        self.pub_date = datetime.fromisoformat(pubDate) if pubDate else None
        self.podcast = Podcast(**podcast) if podcast else None
        # set rest keys as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f"Episode(eid={self.id}, pid={self.pid}, title={self.title})"
