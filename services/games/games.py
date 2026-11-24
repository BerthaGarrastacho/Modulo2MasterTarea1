from config.connections import DatabaseConnection
from fastapi import Request
from models.modelGenres import Genre, Games
from services.twitch import twitch  

# agrega al diccionario del usuario sus juegos favoritos
async def post_fav_games_byID_to_user(user_id:int, myphBD: DatabaseConnection , request: Request):
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

# muestra el listado de juegos en la  tabla de games por orden ascendente
async def get_games_list( myphBD: DatabaseConnection):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor(dictionary=True)
    getQuery = "SELECT * FROM games ORDER BY genre ASC, name ASC"
    mycursor.execute(getQuery)
    res = mycursor.fetchall()
    mycursor.close()
    return res

# transforma la estructura de el listado de juegos favoritos de un usuario en diccionario con los datos del usuario y entro de este, el listado de juegos
def transform_data_games(res):
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

# muestra el listado de juegos en la tabla de games organizados por genero
async def get_games_list_by_genre(myphBD: DatabaseConnection):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor(dictionary=True)
    getQuery = "SELECT * FROM games ORDER BY genre ASC, name ASC"
    mycursor.execute(getQuery)
    res = mycursor.fetchall()
    mycursor.close()
    return transform_data_games(res)

#muestra el listado top 5 de streams de los games favoritos del usuario 
async def get_favs_streams_by_user_games_byID(user_id:int, myphBD: DatabaseConnection , request: Request):
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

# muestra el listado de juegos en la tabla de games organizados por genero
async def get_games_list_by_genre(myphBD: DatabaseConnection):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor(dictionary=True)
    getQuery = "SELECT * FROM games ORDER BY genre ASC, name ASC"
    mycursor.execute(getQuery)
    res = mycursor.fetchall()
    mycursor.close()
    return transform_data_games(res)


# async def post_fav_chanels_byID_to_user(user_id, myphBD, request):
#     mydbConnection = await myphBD.get_db_connection()
#     mycursor = mydbConnection.cursor(dictionary=True)
#     data = await request.json()
#     game_ids = data.get("games", [])
#     getQuery = "Select u.name , g.name FROM users u JOIN user_games ug ON u.id = ug.user_id JOIN games g ON g.id = ug.game_id WHERE u.id = %s"
#     mycursor.execute(getQuery, (user_id,))
#     favorite_games = mycursor.fetchall()
#     mycursor.close()
#     res = []

#     for game in favorite_games:
#         streams = await twitch.get_top_streams_in_game(game["name"])
#         res.append({"game": game["name"], "streams": streams })                             
#     return res