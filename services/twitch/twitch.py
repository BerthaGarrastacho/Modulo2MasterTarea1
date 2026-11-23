import asyncio
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
# llamada buscar la categoria y devuelve un obj de la que hay que sacar el id

async def get_top_stream_in_category(id_cat: str, twitch: Twitch):
    streams = []
    async for stream in twitch.get_streams(game_id=[id_cat], first=5):
        streams.append(stream)
        if len(streams) == 5:
            break
    return streams

async def get_top_streams_in_game(game: str):
    twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
    category_id = await get_id_category(game, twitch) 
    streams = await get_top_stream_in_category(category_id, twitch)
    await twitch.close()
    return streams


async def main():
    twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)  

    print("Top categories:")
    async for game in twitch.get_top_games(first=10):
        print(game.id, game.name)

    print("Search 'mine':")
    async for cat in twitch.search_categories("mine", first=5):
        print(cat.id, cat.name)

    print("By exact name:")
    async for game in twitch.get_games(names=["Minecraft", "Just Chatting"]):
        print(game.id, game.name)

    print("Top live streams in Just Chatting:")
    async for s in twitch.get_streams(game_id=["509658"], first=5):
        print(s.user_name, s.viewer_count)

    await twitch.close()

if __name__ == "__main__":
    asyncio.run(main())