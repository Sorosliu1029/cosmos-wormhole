import httpx


class Subscription:
    def __init__(self, client: httpx.AsyncClient) -> None:
        assert client, "Client must be provided."
        self.client = client

    def list(self):

