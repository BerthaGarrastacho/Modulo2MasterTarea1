from fastapi import FastAPI, Request, Body, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from models.modelPH import Photograper
from config.connections import DatabaseConnection
import os


app= FastAPI()
app.title = "API de Fotógrafos"
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
@app.get('/photograpers', tags=['photograpers'], status_code=200)
async def getPhotographers():
    mydbConnection = await myphBD.get_db_connection()
    phcursor = mydbConnection.cursor(dictionary=True)
    getQuery = "SELECT * FROM photographers"
    phcursor.execute(getQuery)
    res = phcursor.fetchall()
    phcursor.close()
    return res
#CRUD POST
@app.post('/photograpers', tags=['photograpers'], status_code=201)
async def postPhotographer(request: Request):
    mydbConnection = await myphBD.get_db_connection()
    phcursor = mydbConnection.cursor()
    data = await request.json()
    postQuery = "INSERT INTO photographers (name, username, email) VALUES (%s, %s, %s)"
    phcursor.execute(postQuery, (data["name"], data["username"], data["email"]))
    mydbConnection.commit()
    inserted_id = phcursor.lastrowid
    phcursor.close()
    return JSONResponse(
        content={"message": "Fotografo agregado", "id": inserted_id},
        status_code=201
    )
#CRUD PUT
@app.put('/photograpers/{userph_id}', tags=['photograpers'], status_code=200)
async def updatePhotographer(userph_id: int, request: Request):
    mydbConnection = await myphBD.get_db_connection()
    phcursor = mydbConnection.cursor()
    data = await request.json()
    camposActualizados = {}
    for campo in ("name", "username", "email"):
        if campo in data:
            camposActualizados[campo] = data[campo]

    if not camposActualizados:
        phcursor.close()
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")

    fields = ", ".join(f"{campo} = %s" for campo in camposActualizados)
    values = list(camposActualizados.values())
    values.append(userph_id)
    updQuery = f"UPDATE photographers SET {fields} WHERE id = %s"
    phcursor.execute(updQuery, values)
    mydbConnection.commit()
    if phcursor.rowcount == 0:
         phcursor.close()
         raise HTTPException(status_code=404, detail="Fotografo no encontrado")
    phcursor.close()
    return JSONResponse(
         content={"message": "Datos de fotografo actualizado"}, status_code=200)
#CRUD DELETE
@app.delete('/photograpers/{userph_id}', tags=['photograpers'], status_code=200)
async def deletePhotographer(userph_id: int):
    mydbConnection = await myphBD.get_db_connection()
    phcursor = mydbConnection.cursor()
    delQuery = "DELETE FROM `photographers` WHERE id = %s"
    phcursor.execute(delQuery, (userph_id,))
    mydbConnection.commit()
    if phcursor.rowcount == 0:
        phcursor.close()
        raise HTTPException(status_code=404, detail="Fotografo no encontrado")
    phcursor.close()
    return JSONResponse(content={"message": "Fotografo eliminado"},status_code=200)