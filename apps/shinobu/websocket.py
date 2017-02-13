import websockets
import asyncio
import json
import pymysql
from isogen.settings import DATABASES
import logging
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

stickynotes = {}
deleted_notes = []

def fetch_all_notes():
    global stickynotes
    cursor.execute("SELECT * FROM shinobu_stickynote")
    for note in cursor.fetchall():
        stickynotes[note['id']] = note

async def send_to_all(clients, message):
    remove = []
    for socket in clients:
        try:
            await socket.send(message)
        except:
            remove.append(socket)
    for sock in remove:
        clients.remove(sock)

async def send_to_all_except(clients, except_client, message):
    for socket in clients:
        try:
            if socket != except_client:
                await socket.send(message)
        except:
            pass

async def notify(clients, text):
    message = {
        "text":text,
        "action":"notify"
    }
    await send_to_all(clients, json.dumps(message))

async def save_notes_to_database():
    global stickynotes, cursor
    await asyncio.sleep(10)
    for note in stickynotes.values():
        cursor.execute("UPDATE shinobu_stickynote "
                       "SET content=%s, style=%s, x=%s, y=%s, z=%s "
                       "WHERE id=%s",
                       (note['content'],
                        note['style'],
                        int(note['x']),
                        int(note['y']),
                        int(note['z']),
                        int(note['id'])))
    if len(deleted_notes) > 0:
        sql = "DELETE FROM shinobu_stickynote WHERE id IN ({})".format(",".join([str(x) for x in deleted_notes]))
        print(sql)
        cursor.execute(sql)
    connection.commit()
    print("saved to database")


async def handler(websocket:websockets.WebSocketClientProtocol, path):
    global cursor
    print("Client connect: {}".format(websocket.remote_address))
    clients.add(websocket)
    for note in stickynotes:
        nmessage = dict(**stickynotes[note])
        nmessage['action'] = "alter"
        await websocket.send(json.dumps(nmessage))
    try:
        while 1:
            message = json.loads(await websocket.recv())
            action = message['action']
            if action == "new":
                print(action)
                cursor.execute("INSERT INTO shinobu_stickynote "
                               "(content, style, x, y, z) "
                               "VALUES(%s, %s, %s, %s, %s)",
                               (message['content'], message['style'], int(message['x'][:1]), int(message['y'][:1]), int(message['z']),))
                id = connection.insert_id()
                connection.commit()
                notes_obj = {
                                "id":id,
                                "x":message['x'],
                                "y":message['y'],
                                "z":message['z'],
                                "style":message['style'],
                                "content":message['content']
                            }
                stickynotes[id] = notes_obj
                await send_to_all(clients, json.dumps(dict(**notes_obj, action='alter')))
            elif action == "alter":
                note_id = message['id']
                stickynotes[note_id]['x'] = message['x']
                stickynotes[note_id]['y'] = message['y']
                stickynotes[note_id]['z'] = message['z']
                stickynotes[note_id]['style'] = message['style']
                stickynotes[note_id]['content'] = message['content']

                await send_to_all(clients, json.dumps(dict(**stickynotes[note_id], action='alter')))

            elif action == "delete":
                note_id = message['id']
                del stickynotes[note_id]
                deleted_notes.append(int(note_id))
                message = {
                    "action":"delete",
                    "id":note_id
                }
                await send_to_all(clients, json.dumps(message))
                await notify([x for x in clients if x != websocket], "A Note has been deleted")

    except websockets.exceptions.ConnectionClosed as e:
        clients.remove(websocket)


clients = set()
db = DATABASES['default']
connection = pymysql.Connect(host=db['HOST'],
                             user=db['USER'],
                             password=db['PASSWORD'],
                             database=db['NAME'],
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

fetch_all_notes()
print(stickynotes)
asyncio.ensure_future(save_notes_to_database())
start_server = websockets.serve(handler, 'localhost', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
