from fastapi import FastAPI, Request, Body, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from models.modelUser import User
from models.modelGenres import Genre, Games
from config.connections import DatabaseConnection
from twitch import twitch  
import os


app= FastAPI()
app.title = "API de Gestion de Usuarios"
app.version = "0.0.1"

myphBD = DatabaseConnection(
        host="localhost", user="mysql", password="admin", database="user-ph"
    )

@app.get('/', tags=['Home'])
def home():
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Aplicacion FastAPI</title>
            <style>
                body {
                    min-height: 100vh;
                    margin: 0;
                    display: grid;
                    place-items: center;
                    background: #622133;
                    background: linear-gradient(54deg,rgba(98, 33, 51, 1) 0%, rgba(249, 213, 245, 1) 51%, rgba(98, 33, 51, 1) 100%);
                    font-family: Arial, sans-serif;
                }

                .card {
                    max-width: 500px;
                    margin: 20px;
                    padding: 32px;
                    border-radius: 16px;
                    background: white;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
                    text-align: center;
                }

                .card h1 {
                    margin-top: 0;
                    color: #622133;
                }

                .card p {
                    color: #622133;
                }

                .card a {
                    display: inline-block;
                    margin-top: 12px;
                    padding: 10px 18px;
                    border-radius: 8px;
                    background: #622133;
                    color: white;
                    text-decoration: none;
                }

                .card a:hover {
                    background: #F9D5F5;
                    color: #622133;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>Modulo 2 - tarea 1</h1>
                <p>Bienvenido a la api desarrollada con FastAPI.</p>
                <a href="/docs">Abrir la Docs</a>
            </div>
        </body>
        </html>
        """
    )


#CRUD GET
@app.get('/users', tags=['users'], status_code=200)
async def getUsers():
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor(dictionary=True)
    getQuery = "SELECT * FROM users"
    mycursor.execute(getQuery)
    res = mycursor.fetchall()
    mycursor.close()
    return res

#CRUD POST
@app.post('/users', tags=['users'], status_code=201)
async def postUser(request: Request):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor()
    data = await request.json()
    postQuery = "INSERT INTO users (name, username, email) VALUES (%s, %s, %s)"
    mycursor.execute(postQuery, (data["name"], data["username"], data["email"]))
    mydbConnection.commit()
    inserted_id = mycursor.lastrowid
    mycursor.close()
    return JSONResponse(
        content={"message": "user agregado", "id": inserted_id},
        status_code=201
    )

#CRUD PUT
@app.put('/users/{userph_id}', tags=['users'], status_code=200)
async def updateUser(userph_id: int, request: Request):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor()
    data = await request.json()
    camposActualizados = {}
    for campo in ("name", "username", "email"):
        if campo in data:
            camposActualizados[campo] = data[campo]

    if not camposActualizados:
        mycursor.close()
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")

    fields = ", ".join(f"{campo} = %s" for campo in camposActualizados)
    values = list(camposActualizados.values())
    values.append(userph_id)
    updQuery = f"UPDATE users SET {fields} WHERE id = %s"
    mycursor.execute(updQuery, values)
    mydbConnection.commit()
    if mycursor.rowcount == 0:
         mycursor.close()
         raise HTTPException(status_code=404, detail="user no encontrado")
    mycursor.close()
    return JSONResponse(
         content={"message": "Datos de user actualizado"}, status_code=200)

#CRUD DELETE
@app.delete('/users/{userph_id}', tags=['users'], status_code=200)
async def deleteUser(userph_id: int):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor()
    delQuery = "DELETE FROM `users` WHERE id = %s"
    mycursor.execute(delQuery, (userph_id,))
    mydbConnection.commit()
    if mycursor.rowcount == 0:
        mycursor.close()
        raise HTTPException(status_code=404, detail="user no encontrado")
    mycursor.close()
    return JSONResponse(content={"message": "user eliminado"},status_code=200)

# agrega los juegos a un usuario
@app.post('/users/{user_id}/games', tags=['user'], status_code=200)
async def postUserFavGames(user_id:int, request: Request):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor()
    data = await request.json()
    rows = [(user_id, game_id) for game_id in data["games"]]
    mycursor.executemany(
    "INSERT INTO user_games (user_id, game_id) VALUES (%s, %s)",
    rows
    )
    mydbConnection.commit()
    inserted = mycursor.rowcount
    mycursor.close()
    return JSONResponse(
       content={"message": "juegos agregados", "inserted": inserted},
        status_code=200
    )
#  muestra el listado de juegos ordenados ascendentemente
@app.get('/games', tags=['games'], status_code=200)
async def get_games_list():
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor(dictionary=True)
    getQuery = "SELECT * FROM games ORDER BY genre ASC, name ASC"
    mycursor.execute(getQuery)
    res = mycursor.fetchall()
    mycursor.close()
    return res
#  muestra el listado de juegos organizados por genero
@app.get('/games/genre', tags=['games'], status_code=200)
async def get_games_list_by_genre():
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor(dictionary=True)
    getQuery = "SELECT * FROM games ORDER BY genre ASC, name ASC"
    mycursor.execute(getQuery)
    res = mycursor.fetchall()
    mycursor.close()
    return transform_data(res)

def transform_data(res):
    list_genre = []
    for juego in res:
        if not juego["genre"] in list_genre:
            list_genre.append(juego["genre"])
        # print(juego["id"], juego["name"], juego["genre"])

    list_obj_genres = []
    for genre in list_genre:
        list_obj_genres.append(
            Genre(genre = genre, games=[])
        )

    for juego in res:
        for genre in list_obj_genres:
            if juego["genre"] == genre.genre:
                genre.games.append(
                    Games(id = juego["id"], name = juego["name"])
                )
    return list_obj_genres

# devuelve el listado de los juegos favoritos del usuario
@app.get('/user-fav-games/{user_id}', tags=['users'], status_code=200)
async def get_fav_games_byID(user_id:int, request: Request):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor(dictionary=True)
    data = await request.json()
    game_ids = data.get("games", [])
    getQuery = "Select u.name , g.name FROM users u JOIN user_games ug ON u.id = ug.user_id JOIN games g ON g.id = ug.game_id WHERE u.id = %s"
    mycursor.execute(getQuery, (user_id,))
    favorite_games = mycursor.fetchall()
    mycursor.close()

    res = []
    for game in favorite_games:
        streams = await twitch.get_top_streams_in_game(game["name"])
        res.append({"game": game["name"], "streams": streams })
                                                
    return res
