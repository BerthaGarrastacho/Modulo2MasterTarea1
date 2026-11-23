from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from config.connections import DatabaseConnection
from services.users import users
from services.games import games

import os

app= FastAPI()
app.title = "API de Gestion de Usuarios"
app.version = "0.0.3"

myphBD = DatabaseConnection( host="localhost", user="mysql", password="admin", database="user-ph")

#CRUD GET HOME CLEAN ARCH
@app.get('/', tags=['Home'])
def get_Home():
    return users.home()

#CRUD GET USER CLEAN ARCH
@app.get('/users', tags=['users'], status_code=200)
async def getUsers():
    return await users.getUsers(myphBD)

#CRUD POST USER CLEAN ARCH
@app.post('/users', tags=['users'], status_code=201)
async def postUser(request: Request):
    return await users.postUser(myphBD, request)

#CRUD PUT USER CLEAN ARCH
@app.put('/users/{userph_id}', tags=['users'], status_code=200)
async def updateUser(userph_id: int, request: Request):
    return await users.updateUser(userph_id, myphBD, request)

#CRUD DELETE USER CLEAN ARCH
@app.delete('/user/{userph_id}', tags=['users'], status_code=200)
async def deleteUser(userph_id: int):
    return await users.deleteUser(userph_id, myphBD)

# CRUD POST GAMES TO USERS CLEAN ARCH - agrega a una usuario sus juegos favoritos
@app.post('/user/{user_id}/games', tags=['user'], status_code=200)
async def postUserFavGames(user_id:int, request: Request):
   return await games.post_fav_games_byID_to_user(user_id, myphBD, request)

# CRUD GET GAMES BY ASC CLEAN ARCH -  muestra el listado de juegos ordenados ascendentemente
@app.get('/games', tags=['games'], status_code=200)
async def get_list_games_asc():
   return await games.get_games_list(myphBD)

# CRUD GET GAMES BY GENRE CLEAN ARCH  muestra el listado de juegos organizados por genero
@app.get('/games/genre', tags=['games'], status_code=200)
async def get_list_games_by_genre():
    return await games.get_games_list_by_genre(myphBD)

# CRUD GET STREAMS BY FAVS GAMES TO USER -  devuelve el listado de los juegos favoritos del usuario
@app.get('/user-fav-games/{user_id}', tags=['users'], status_code=200)
async def get_list_streams_favs_by_fav_games_cat(user_id: int):
    return await games.get_favs_streams_by_user_games_byID(user_id, myphBD)
