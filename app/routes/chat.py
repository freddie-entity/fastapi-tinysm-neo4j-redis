from typing import List, Tuple, Dict
import aioredis
from fastapi import APIRouter, WebSocket
from models.chat import MessageContent
from fastapi.param_functions import Body
from config import settings
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/sendmessage")
async def send_chat_message(stream: str, data: dict = Body(...)):
    print(jsonable_encoder(data))
    redis = await aioredis.from_url(settings.DB_REDIS_CACHE)
    flag = await redis.xadd(stream, jsonable_encoder(data))
    if flag:
        return {"message": "Send message successfully!"}
    return {"error": "Fail while sending message."}

# stream_name, message_id, dict of key->value pairs in message
Message = Tuple[bytes, bytes, Dict[bytes, bytes]]

@router.websocket("/ws/{stream}")
async def websocket_endpoint(websocket: WebSocket, stream: str = None, last_n: int = 20):
    print('a new websocket to create.')
    await websocket.accept()
    redis = await aioredis.from_url(settings.DB_REDIS_CACHE)
    while True:
        try:
            # Call read_from_stream, and return if it raises an exception
            messages: List[Message]
            read = 0
            try:
                messages = await read_from_stream(redis, stream, None, None, last_n)
            except Exception as e:
                continue

            # If we have no new messages, note that read timed out and return
            if len(messages) < 1:
                continue


            # # Prepare messages (message_id and JSON-serializable payload dict)
            prepared_messages = {"data": []}
            if len(messages) > 0:
                for msg in messages:
                    latest_id = msg[1].decode("utf-8")
                    payload = {k.decode("utf-8"): v.decode("utf-8") for k, v in msg[2].items()}
                    prepared_messages['data'].append({"message_id": latest_id, "payload": payload})
                read = len(messages)
                
                            
            await websocket.receive_text()
            await websocket.send_json(prepared_messages)
            
            
        except Exception as e:
            print('error:', e)
            break
    print('Bye..')

async def read_from_stream(
    redis: aioredis.Redis, stream: str, latest_id: str = None, past_ms: int = None, last_n: int = None
) -> List[Message]:
    timeout_ms = 60 * 1000

    # Blocking read for every message added after latest_id, using XREAD
    if latest_id is not None:
        return await redis.xread([stream], latest_ids=[latest_id], timeout=timeout_ms)

    # Blocking read for every message added after current timestamp minus past_ms, using XREAD
    if past_ms is not None:
        server_time_s = await redis.time()
        latest_id = str(round(server_time_s * 1000 - past_ms))
        return await redis.xread([stream], latest_ids=[latest_id], timeout=timeout_ms)

    # Non-blocking read for last_n messages, using XREVRANGE
    if last_n is not None:
        messages = await redis.xrevrange(stream, count=last_n)
        return list(reversed([(stream.encode("utf-8"), *m) for m in messages]))

    # Default case, blocking read for all messages added after calling XREAD
    return await redis.xread([stream], timeout=timeout_ms)


