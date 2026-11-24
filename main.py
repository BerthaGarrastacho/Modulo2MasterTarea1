from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from config.connections import DatabaseConnection
from services.users import users
from services.games import games
from services.channels import channel

import os

app= FastAPI()
app.title = "API de Gestion de Usuarios y sus preferencias en Twitch"
app.version = "0.0.4"

myphBD = DatabaseConnection( host="localhost", user="mysql", password="admin", database="user-ph")

#CRUD GET HOME CLEAN ARCH
@app.get('/', tags=['Home'])
def get_Home():
    return users.get_Home()

#CRUD GET USER CLEAN ARCH -  devyelde todos los usuarios con su estrcutura completa
@app.get('/users', tags=['users'], status_code=200)
async def getUsers():
    return await users.getUsers(myphBD)

#CRUD POST USER CLEAN ARCH -  agrea un nuevo usuario
@app.post('/users', tags=['users'], status_code=201)
async def postUser(request: Request):
    return await users.postUser(myphBD, request)

#CRUD PUT USER CLEAN ARCH -  actualiza datos de un usuario (name, email, username)
@app.put('/users/{userph_id}', tags=['users'], status_code=200)
async def updateUser(userph_id: int, request: Request):
    return await users.updateUser(userph_id, myphBD, request)

#CRUD DELETE USER CLEAN ARCH - elimina un usuario por ID
@app.delete('/user/{userph_id}', tags=['users'], status_code=200)
async def deleteUser(userph_id: int):
    return await users.deleteUser(userph_id, myphBD)

# CRUD GET GAMES BY ASC CLEAN ARCH -   muestra el listado de juegos ordenados ascendentemente
@app.get('/games', tags=['games'], status_code=200)
async def get_list_games_asc():
   return await games.get_games_list(myphBD)

# CRUD GET GAMES BY GENRE CLEAN ARCH -   muestra el listado de juegos organizados por genero
@app.get('/games/genre', tags=['games'], status_code=200)
async def get_list_games_by_genre():
    return await games.get_games_list_by_genre(myphBD)

# CRUD GET FAVS GAMES TO USER CLEAN ARCH -  devuelve el listado de los juegos favoritos del usuario
@app.get('/user-fav-games/{user_id}', tags=['games'], status_code=200)
async def get_games_list_fav_to_user(user_id: int):
    return await games.get_games_list_fav_to_user(myphBD, user_id)

# CRUD POST STREAMS TOP 3 TO USER FAV GAMES GENRE CLEAN ARCH - agrega a una usuario sus juegos favoritos
@app.post('/user/{user_id}/games', tags=['games'], status_code=200)
async def postUserFavGames(user_id:int, request: Request):
   return await games.post_fav_games_byID_to_user(user_id, myphBD, request)

# CRUD GET TOP CHANNELS CLEAN ARCH -  muestra el listado de canales de la tabla Chanels
@app.get('/channels', tags=['channels'], status_code=200)
async def get_list_channels():
   return await channel.get_channel_list(myphBD)

# CRUD POST STREAMERS TO USER GENRE CLEAN ARCH - agrega a una usuario sus canales favoritos
@app.post('/user/{user_id}/channels', tags=['channels'], status_code=200)
async def postUserFavChannels(user_id:int, request: Request):
   return await channel.post_fav_channels_byID_to_user(user_id, myphBD, request)

# CRUD GET FAVS CHANNELS TO USER CLEAN ARCH -  devuelve el listado de los canales favoritos del usuario
@app.get('/user-fav-channels/{user_id}', tags=['games'], status_code=200)
async def get_games_list_fav_to_user(user_id: int):
    return await channel.get_chanels_list_fav_to_user(myphBD, user_id)

# CRUD GET FAVS CHANNELS ARE ON LIVE CLEAN ARCH -  muestra cuales de los canales favoritos del usuario est'a en vivo
@app.get('/user-fav-channels-ONLIVE/{user_id}', tags=['games'], status_code=200)
async def get_channel_onlive_to_user_fav_channels(user_id: int):
    return await channel.get_live_fav_channels_by_user(user_id, myphBD)

