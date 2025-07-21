from .base import ListBase


class Playlist(ListBase[str]):
    entity_class = str
    endpoint = "/v1/playlist"
    list_suffix = "pull"

    def _extract_data(self, json_resp: dict) -> list[dict]:
        data = json_resp.get("data", {})
        return data.get("list", [])
