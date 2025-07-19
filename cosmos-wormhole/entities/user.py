from typing import Any

from .base import Base


class User(Base):
    def __init__(
        self,
        uid: str,
        nickname: str,
        avatar: dict[str, Any] = {},
        bio: str = "",
        gender: str = "",
        **kwargs,
    ):
        super().__init__(id=uid)
        self.nickname = nickname
        self.avatar = avatar
        self.bio = bio
        self.gender = gender
        # set rest keys as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f"User(uid={self.id}, nickname={self.nickname})"
