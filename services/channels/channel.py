from config.connections import DatabaseConnection
from fastapi import Request
from services.twitch import twitch  

# muetsra el listado de juegos en la  tabla de games por orden ascendente
async def get_channel_list( myphBD: DatabaseConnection):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor(dictionary=True)
    getQuery = "SELECT * FROM channels"
    mycursor.execute(getQuery)
    res = mycursor.fetchall()
    mycursor.close()
    return res

# agerga al usuario sus canales favoritos en la tabla user_channels
async def post_fav_channels_byID_to_user(user_id:int, myphBD: DatabaseConnection, request: Request):
    data = await request.json()
    channel_ids = data.get("channels", [])
    if not channel_ids:
        return {"message": "no se enviaron canales", "inserted": 0}

    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor()
    postQuery = "INSERT IGNORE INTO user_channels (user_id, channel_id) VALUES (%s, %s)"
    mycursor.executemany(postQuery, [(user_id, channel_id) for channel_id in channel_ids])
    mydbConnection.commit()
    inserted = mycursor.rowcount
    mycursor.close()
    return {"message": "canales agregados", "inserted": inserted}

# muetsra los channels favoritos del usuario
# este metodo es para transformar la estructura en un dic user: {channels: [list of channels]}
def transform_data_channels(res):
    return [
        {"id": row["channel_id"], "name": row["name"]}
        for row in res
        if row["name"] is not None
    ]
# muestra el listado de canales favoritos de un usuario
async def get_chanels_list_fav_to_user(myphBD: DatabaseConnection, user_id:int):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor(dictionary=True)
    getQuery = """
    SELECT u.username, c.id AS channel_id, c.name AS name
    FROM users u
    LEFT JOIN user_channels uc ON uc.user_id = u.id
    LEFT JOIN channels c ON c.id = uc.channel_id
    WHERE u.id = %s
    ORDER BY c.name ASC
    """
    mycursor.execute(getQuery, (user_id,))
    rows = mycursor.fetchall()
    mycursor.close()

    if not rows:
        return {}

    username = rows[0]["username"]
    channels = transform_data_channels(rows)
    return {username: {"channels": channels}}

# muestra cuales de los canales favoritos del usuario estan en vivo
async def get_live_fav_channels_by_user(user_id: int, myphBD: DatabaseConnection):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor(dictionary=True)
    getQuery = """
    SELECT c.name
    FROM user_channels uc
    JOIN channels c ON c.id = uc.channel_id
    WHERE uc.user_id = %s
    """
    mycursor.execute(getQuery, (user_id,))
    names = [row["name"] for row in mycursor.fetchall() if row["name"]]
    mycursor.close()

    if not names:
        return {"live": []}

    logins = [name.lower() for name in names]
    live = await twitch.get_top_channels_on_live(logins)
    return {"live": live}
