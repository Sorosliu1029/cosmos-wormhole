import asyncio

import httpx
from endpoints import *
from managers import *


class Client:
    # TODO: read version
    user_agent = "CosmosWormhole/0.0.1"
    device_id = "cosmos-wormhole"

    def __init__(self, base_url: str = "https://api.xiaoyuzhoufm.com") -> None:
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={"user-agent": self.user_agent, "x-jike-device-id": self.device_id},
        )
        self.token_manager = TokenManager()
        self.token_update_queue = asyncio.Queue(2)
        self.token_update_producer: asyncio.Task
        self.token_update_consumer: asyncio.Task

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

    def _init_endpoints(self) -> None:
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

    async def close(self) -> None:
        await self.token_update_queue.join()

        tasks = [self.token_update_producer, self.token_update_consumer]
        for task in tasks:
            if task and not task.done():
                task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

        await self.client.aclose()

    def _update_token(self, access_token: str, refresh_token: str) -> None:
        if not access_token or not refresh_token:
            raise ValueError("Access token and refresh token cannot be empty.")
        self.token_manager.save_token(
            access_token=access_token, refresh_token=refresh_token
        )
        self.client.headers.update(
            {Token.access_key: access_token, Token.refresh_key: refresh_token}
        )

    async def login(self) -> None:
        headers = self.token_manager.get_token()

        if (
            not headers
            or not headers.get(Token.access_key)
            or not headers.get(Token.refresh_key)
        ):  # first time or no token stored or token invalid, try to login
            access_token, refresh_token = await Login().login()
            self._update_token(access_token, refresh_token)
        else:  # refresh tokens in case of access token expired
            self.client.headers.update(headers)
            access_token, refresh_token = await self.token_manager.refresh_token(
                self.client
            )
            self._update_token(access_token, refresh_token)

        self.after_login()

    def after_login(self) -> None:
        self.token_update_producer = asyncio.create_task(
            self.token_manager.periodic_refresh_token(
                self.client, 60 * 1, self.token_update_queue
            )  # every 20 minutes
        )
        self.token_update_consumer = asyncio.create_task(self._listen_on_token_update())
        self._init_endpoints()

    async def _listen_on_token_update(self) -> None:
        try:
            while True:
                access_token, refresh_token = await self.token_update_queue.get()
                self._update_token(access_token, refresh_token)
                self.token_update_queue.task_done()
        except asyncio.CancelledError:
            pass


async def main():
    c = Client()
    await c.login()

    print("1. Subscription:")
    pid = None
    eid = None
    podcast_uid = None
    async for podcast in c.subscription.list():
        print(podcast)
        if podcast.title == "史蒂夫说":
            pid = podcast.id
            podcast_uid = podcast.podcasters[0].id if podcast.podcasters else None
            async for episode in c.episode.list_by_podcast(podcast.id):
                print(f"\t{episode}")
                eid = episode.id
                async for comment in c.comment.list_by_episode(episode.id, "HOT"):
                    print(f"\t\t{comment}")
                    async for reply in c.reply.list_by_comment(comment.id, "SMART"):
                        print(f"\t\t\t{reply}")
                    break
                break
            break

    print("2. Podcaast/Episode get:")
    if pid:
        podcast = await c.podcast.get(pid)
        print(podcast)
    if eid:
        episode = await c.episode.get(eid)
        print(episode)

    print("3. Inbox:")
    cnt = 0
    async for episode in c.inbox.list():
        print(episode)
        cnt += 1
        if cnt >= 5:
            break

    print("4. Playlist:")
    cnt = 0
    async for playlist in c.playlist.list():
        print(playlist)
        cnt += 1
        if cnt >= 5:
            break

    print("5. Profile:")
    my_profile = await c.profile.get()
    print(my_profile)

    if podcast_uid:
        print("5.1 Podcaster Profile:")
        podcaster = await c.profile.get(podcast_uid)
        print(podcaster)

    print("6. Followee:")
    cnt = 0
    async for user in c.followee.list_following(my_profile.id):
        print(user)
        cnt += 1
        if cnt >= 5:
            break

    print("7. Follower:")
    cnt = 0
    async for user in c.follower.list_follower(my_profile.id):
        print(user)
        cnt += 1
        if cnt >= 5:
            break

    print("8. History:")
    cnt = 0
    async for episode in c.history.list():
        print(episode)
        cnt += 1
        if cnt >= 5:
            break

    print("9. Favorited Episode:")
    cnt = 0
    async for episode in c.favorited_episode.list():
        print(episode)
        cnt += 1
        if cnt >= 5:
            break

    await c.close()


if __name__ == "__main__":
    asyncio.run(main())
