from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from config.connections import DatabaseConnection
from models.modelUser import User
from database import database

#CRUD GET HOME Logic
def get_Home():
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

#CRUD GET USERS Logic
async def getUsers(myphBD: DatabaseConnection): 
    users_with_games = await database.get_user_with_games(myphBD)
    users_with_channels = await database.get_user_with_channels(myphBD)
    usuarios = {}
    for row in users_with_games:
        usuario = usuarios.setdefault(row["id"], {
            "id": row["id"],
            "name": row["name"],
            "username": row["username"],
            "email": row["email"],
            "games": [],
            "channels": [],
        })
        if row["game_id"] is not None:
            usuario["games"].append({"id": row["game_id"], "name": row["game_name"]})

    for row in users_with_channels:
        if row["id"] in usuarios and row["channel_id"] is not None:
            usuarios[row["id"]]["channels"].append({"id": row["channel_id"], "name": row["channel_name"]})

    return list(usuarios.values())

#CRUD GET USER BY ID Logic
async def get_user_by_id(userph_id: int, myphBD: DatabaseConnection):
    user = await database.find_user_by_id(myphBD, userph_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user no encontrado")

    games = await database.get_games_by_user_id(myphBD, userph_id)
    channels = await database.get_channels_by_user_id(myphBD, userph_id)
    return {
        "id": user["id"],
        "name": user["name"],
        "username": user["username"],
        "email": user["email"],
        "games": [{"id": g["id"], "name": g["name"]} for g in games],
        "channels": [{"id": c["id"], "name": c["name"]} for c in channels],
    }

#CRUD POST USER Logic    
async def postUser(myphBD: DatabaseConnection, request: Request):
    usuario: User = await request.json()
    inserted_id =  await database.insert_users(myphBD, usuario)
    return JSONResponse(
        content={"message": "user agregado", "id": inserted_id},
        status_code=201
    )

#CRUD PUT USER Logic   
async def updateUser(userph_id: int, myphBD: DatabaseConnection, request: Request):
    data = await request.json()
    campos_actualizados = {}
    for campo in ("name", "username", "email"):
        if campo in data:
            campos_actualizados[campo] = data[campo]

    if not campos_actualizados:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")

    if await database.find_id_user(myphBD, userph_id) is None:
        raise HTTPException(status_code=404, detail="user no encontrado")

    await database.update_user(myphBD, userph_id, campos_actualizados)
    return JSONResponse(
         content={"message": "Datos de user actualizado"}, status_code=200)

#CRUD DELETE USER Logic   
async def deleteUser( userph_id: int , myphBD: DatabaseConnection):

    if await database.delete_user(myphBD, userph_id) == 0:
        raise HTTPException(status_code=404, detail="user no encontrado")

    return JSONResponse(content={"message": "user eliminado"},status_code=200)