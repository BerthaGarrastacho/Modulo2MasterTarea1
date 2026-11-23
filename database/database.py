from config.connections import DatabaseConnection
from models.modelUser import User

async def get_user_with_games(myphBD: DatabaseConnection):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor(dictionary=True)
    getQuery = """
    SELECT u.id, u.name, u.username, u.email,
           g.id AS game_id, g.name AS game_name
    FROM users u
    LEFT JOIN user_games ug ON ug.user_id = u.id
    LEFT JOIN games g ON g.id = ug.game_id
    ORDER BY u.id
    """
    mycursor.execute(getQuery)
    users_with_games = mycursor.fetchall()
    mycursor.close()
    return users_with_games

async def insert_users(myphBD: DatabaseConnection, usuario: User):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor()
    postQuery = "INSERT INTO users (name, username, email) VALUES (%s, %s, %s)"
    mycursor.execute(postQuery, (usuario["name"], usuario["username"], usuario["email"]))
    mydbConnection.commit()
    inserted_id = mycursor.lastrowid
    mycursor.close()
    return inserted_id

async def update_user(myphBD: DatabaseConnection, userph_id: int, campos_actualizados: dict):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor()
    fields = ", ".join(f"{campo} = %s" for campo in campos_actualizados)
    values = list(campos_actualizados.values())
    values.append(userph_id)
    updQuery = f"UPDATE users SET {fields} WHERE id = %s"
    mycursor.execute(updQuery, values)
    mydbConnection.commit()
    mycursor.close()


async def find_id_user(myphBD: DatabaseConnection, userph_id: int):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor()

    mycursor.execute("SELECT id FROM users WHERE id = %s", (userph_id,))
    user_id = mycursor.fetchone()
    mycursor.close()
    return user_id


async def delete_user(myphBD: DatabaseConnection, userph_id: int):
    mydbConnection = await myphBD.get_db_connection()
    mycursor = mydbConnection.cursor()
    delQuery = "DELETE FROM `users` WHERE id = %s"
    mycursor.execute(delQuery, (userph_id,))
    mydbConnection.commit()
    p_rowcount =mycursor.rowcount
    mycursor.close()
    return p_rowcount
