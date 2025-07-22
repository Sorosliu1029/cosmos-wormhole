import asyncio

import httpx

from .__about__ import __version__
from .endpoints import *
from .managers import *


class Client:
    user_agent = f"CosmosWormhole/{__version__}"
    device_id = "cosmos-wormhole"

    def __init__(self, base_url: str = "https://api.xiaoyuzhoufm.com") -> None:
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={"user-agent": self.user_agent, "x-jike-device-id": self.device_id},
        )
        self.token_manager = TokenManager()
        self.__token_update_queue = asyncio.Queue(1)
        self.__token_update_producer: asyncio.Task
        self.__token_update_consumer = asyncio.create_task(
            self.__listen_on_token_update()
        )

        self.subscription: Subscription
        self.episode: Episode
        self.comment: Comment
        self.reply: Reply
        self.playlist: Playlist
        self.podcast: Podcast
        self.inbox: Inbox
        self.profile: Profile
        self.followee: Followee
        self.follower: Follower
        self.history: History
        self.favorited_episode: FavoritedEpisode
        self.favorited_comment: FavoritedComment
        self.podcast_search: PodcastSearch
        self.episode_search: EpisodeSearch
        self.user_search: UserSearch

    async def __listen_on_token_update(self) -> None:
        try:
            while True:
                access_token, refresh_token = await self.__token_update_queue.get()
                self.__update_token(access_token, refresh_token)
                self.__token_update_queue.task_done()
        except asyncio.CancelledError:
            pass

    def __update_token(self, access_token: str, refresh_token: str) -> None:
        if not access_token or not refresh_token:
            raise ValueError("Access token and refresh token cannot be empty.")
        self.token_manager.save_token(
            access_token=access_token, refresh_token=refresh_token
        )
        self.client.headers.update(
            {Token.access_key: access_token, Token.refresh_key: refresh_token}
        )

    def __init_endpoints(self) -> None:
        self.subscription = Subscription(self.client)
        self.episode = Episode(self.client)
        self.comment = Comment(self.client)
        self.reply = Reply(self.client)
        self.playlist = Playlist(self.client)
        self.podcast = Podcast(self.client)
        self.inbox = Inbox(self.client)
        self.profile = Profile(self.client)
        self.followee = Followee(self.client)
        self.follower = Follower(self.client)
        self.history = History(self.client)
        self.favorited_episode = FavoritedEpisode(self.client)
        self.favorited_comment = FavoritedComment(self.client)
        self.podcast_search = PodcastSearch(self.client)
        self.episode_search = EpisodeSearch(self.client)
        self.user_search = UserSearch(self.client)

    async def close(self) -> None:
        await self.__token_update_queue.join()

        tasks = [self.__token_update_producer, self.__token_update_consumer]
        for task in tasks:
            if task and not task.done():
                task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

        await self.client.aclose()

    async def login(self) -> None:
        headers = self.token_manager.get_token()

        if (
            not headers
            or not headers.get(Token.access_key)
            or not headers.get(Token.refresh_key)
        ):  # first time or no token stored or token invalid, try to login
            access_token, refresh_token = await Login().login()
            self.__update_token(access_token, refresh_token)
        else:  # refresh tokens in case of access token expired
            self.client.headers.update(headers)
            access_token, refresh_token = await self.token_manager.refresh_token(
                self.client
            )
            self.__update_token(access_token, refresh_token)

        self.__after_login()

    def __after_login(self) -> None:
        self.__token_update_producer = asyncio.create_task(
            self.token_manager.periodic_refresh_token(
                self.client, 60 * 20, self.__token_update_queue
            )  # every 20 minutes
        )
        self.__init_endpoints()
