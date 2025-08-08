import asyncio
import websockets
import json

rooms = {}

async def handler(ws, path):
    room_id = path.strip("/")
    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(ws)

    try:
        async for message in ws:
            for client in rooms[room_id]:
                if client != ws:
                    await client.send(message)
    finally:
        rooms[room_id].remove(ws)
        if not rooms[room_id]:
            del rooms[room_id]

if __name__ == "__main__":
    start_server = websockets.serve(handler, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
