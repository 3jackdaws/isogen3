import websockets
import asyncio
import json
import pymysql
from isogen.settings import DATABASES
import logging
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.WARN)
logger.addHandler(logging.StreamHandler())

async def handler(websocket:websockets.WebSocketClientProtocol, path):
    while 1:
        message = json.loads(await websocket.recv())

        try:
            action = message['action']
            if action == "new":
                cursor = connection.cursor()
                cursor.execute("INSERT INTO shinobu_stickynote "
                               "(content, style, x, y, z) "
                               "VALUES(%s, %s, %s, %s, %s)",
                               (message['content'], message['style'], int(message['x'][:1]), int(message['y'][:1]), int(message['z']),))
                id = connection.insert_id()
                connection.commit()
                for socket in clients:
                    if socket.state is not "CLOSED":
                        await socket.send(json.dumps({
                            "object":"note",
                            "id":id,
                            "x":message['x'],
                            "y":message['y'],
                            "z":message['z'],
                            "style":message['style'],
                            "content":message['content']
                        }))
            elif action == "fetch":
                if websocket not in clients:
                    clients.add(websocket)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM shinobu_stickynote ORDER BY z ASC")
                notes = cursor.fetchall()
                for note in notes:
                    nmessage = dict(**note)
                    nmessage['object'] = "note"
                    await websocket.send(json.dumps(nmessage))
            elif action == "alter":
                cursor = connection.cursor()
                cursor.execute("UPDATE shinobu_stickynote "
                               "SET content=%s, style=%s, x=%s, y=%s, z=%s "
                               "WHERE id=%s",
                               (message['content'],
                                message['style'],
                                int(message['x'][:-2]),
                                int(message['y'][:-2]),
                                int(message['z']),
                                int(message['id'])))
                connection.commit()
                for socket in clients:
                    if socket.state is not "CLOSED":
                        await socket.send(json.dumps({
                            "object": "note",
                            "id": message['id'],
                            "x": message['x'],
                            "y": message['y'],
                            "z": message['z'],
                            "style": message['style'],
                            "content": message['content']
                        }))

        except Exception as e:
            print(e)


clients = set()
db = DATABASES['default']
connection = pymysql.Connect(host=db['HOST'],
                             user=db['USER'],
                             password=db['PASSWORD'],
                             database=db['NAME'],
                             cursorclass=pymysql.cursors.DictCursor)

start_server = websockets.serve(handler, 'localhost', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
