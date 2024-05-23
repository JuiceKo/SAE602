import asyncio
import json
import mysql.connector
from nats.aio.client import Client as NATS
from functools import partial

async def insert_message(cursor, message, conn):
    try:
        cursor.execute("INSERT INTO messages (message) VALUES (%s)", (message,))
        conn.commit()  # Utiliser la connexion pour commettre
    except Exception as e:
        print("An error occurred while inserting message into MySQL:", e)

async def message_handler(msg, cursor, conn):
    subject = msg.subject
    reply = msg.reply

    try:
        data = json.loads(msg.data.decode())
        print("Received message:", data)

        # Insérer le message dans la base de données MySQL
        await insert_message(cursor, json.dumps(data), conn)

        response_data = {"message": "Bonjour, vous avez envoyé : " + data.get("message", "")}
        if reply:
            await msg.respond(json.dumps(response_data).encode())
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    except Exception as e:
        print("An error occurred in message_handler:", e)

async def subscribe_handler(msg, cursor, conn):
    await message_handler(msg, cursor, conn)

async def run():
    # Connexion à la base de données MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="toto",
        database="messages"
    )
    cursor = conn.cursor()
    print("Connected to MySQL database")

    nc = NATS()

    try:
        await nc.connect(servers=["nats://0.0.0.0:4222"])
        print("NATS client connected")

        await nc.subscribe("requete", cb=partial(subscribe_handler, cursor=cursor, conn=conn))
        print("Subscribed to 'requete'")

        # Garder la connexion ouverte
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Failed to connect to NATS server: {e}")
        await nc.close()
    finally:
        cursor.close()
        conn.close()
        print("Closed MySQL and NATS connections")

if __name__ == '__main__':
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Keyboard interrupt received, exiting...")
