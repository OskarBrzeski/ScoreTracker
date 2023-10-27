import os
from datetime import datetime, timedelta, timezone
from time import sleep
from typing import Final

from dotenv import load_dotenv
from ossapi import GameMode, Ossapi, OssapiV1, Score
from ossapi.ossapi import Beatmap as BeatmapV1

load_dotenv(".env")
API_LEGACY_KEY: Final[str] = os.environ.get("LEGACY_OSU_API_KEY")
API_CLIENT_ID: Final[int] = int(os.environ.get("CLIENT_ID"))
API_CLIENT_SECRET: Final[str] = os.environ.get("CLIENT_SECRET")


API_V1 = OssapiV1(API_LEGACY_KEY)
API = Ossapi(API_CLIENT_ID, API_CLIENT_SECRET)


def get_all_leaderboard_maps(
    since: datetime = datetime(2007, 1, 1, tzinfo=timezone.utc),
    upto: datetime = datetime.now(timezone.utc) + timedelta(days=1),
) -> list[BeatmapV1]:
    """Retrieves all maps approved between `since` and `upto` (UTC)"""

    maps: list[BeatmapV1] = []
    map_id_set: set[int] = set()

    while retrieved := API_V1.get_beatmaps(since=since):
        sleep(0.3)
        for map in retrieved:
            if map.beatmap_id in map_id_set:
                continue
            if map.approved_date > upto:
                return maps

            maps.append(map)
            map_id_set.add(map.beatmap_id)

        since = maps[-1].approved_date - timedelta(seconds=1)

    return maps


def get_score(map_id: int, user_id: int) -> Score | tuple[int, int]:
    sleep(0.3)
    print(f"map id: {map_id}")
    try:
        return API.beatmap_user_score(map_id, user_id, mode=GameMode.OSU).score
    except ValueError:
        return (user_id, map_id)
