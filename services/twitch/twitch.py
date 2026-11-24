import os
from pathlib import Path

from dotenv import load_dotenv
from twitchAPI.twitch import Twitch
from twitchAPI.helper import limit

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

async def get_id_category(name: str, twitch: Twitch):
    async for cat in twitch.search_categories(name, first=1):
        return cat.id
    return None

async def get_top_stream_in_category(id_cat: str, twitch: Twitch):
    streams = []
    async for stream in twitch.get_streams(game_id=[id_cat], first=5):
        streams.append(stream)
        if len(streams) == 5:
            break
    return streams

async def get_top_streams_in_game(game: str):
    twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
    try:
        category_id = await get_id_category(game, twitch)
        if category_id is None:
            return []

        streams = await get_top_stream_in_category(category_id, twitch)
        return [
            {
                "user_name": s.user_name,
                "title": s.title,
                "game_name": s.game_name,
                "viewer_count": s.viewer_count,
                "started_at": s.started_at.isoformat(),
                "language": s.language,
            }
            for s in streams
        ]
    finally:
        await twitch.close()

async def get_top_channels_on_live(logins: list[str]):
    live = []
    if not logins:
        return live

    twitch_client = await Twitch(CLIENT_ID, CLIENT_SECRET)
    # la API de Twitch acepta hasta 100 logins por consulta
    for i in range(0, len(logins), 100):
        async for stream in twitch_client.get_streams(user_login=logins[i:i + 100]):
            live.append({
                "channel": stream.user_login,
                "title": stream.title,
                "game": stream.game_name,
                "viewers": stream.viewer_count,
            })
    await twitch_client.close()
    return live
