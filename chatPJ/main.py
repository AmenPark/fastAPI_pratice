from fastapi import FastAPI, WebSocket, Request
from collections import deque
from starlette.websockets import WebSocketDisconnect
import asyncio
from fastapi.templating import Jinja2Templates
app = FastAPI()

templates = Jinja2Templates(directory="templates")
now_in = set()
Q =deque()              # 대기중인 사람 수.
enter_info = [1,0]      # 최대 1명, 0명 입장중

# 웹소켓 연결을 테스트 할 수 있는 웹페이지 (http://127.0.0.1:8000/client)
@app.get("/client")
async def client(request: Request):
    return templates.TemplateResponse("client.html", {"request":request})

# 웹소켓 설정 ws://127.0.0.1:8000/ws 로 접속할 수 있음
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # client의 websocket접속 허용
    if enter_info[0]<=enter_info[1]:
        Q.append(websocket)
        await websocket.send_text(f"{{'waiting':{len(Q)} }}")
        while websocket not in now_in:
            await asyncio.sleep(1)                  # 뭔가 더 깔끔한 방법 쓰고싶은데..

    else:
        enter_info[1]+=1
        now_in.add(websocket)

    await websocket.send_text("입장했습니다.")
    print(websocket.client, "입장")
    while True:
        try:
            data = await websocket.receive_text()  # client 메시지 수신대기
            for ws in now_in:
                await ws.send_text(f"client {websocket.client}: {data}")
            print(f"message received : {data} from : {websocket.client}")
        except WebSocketDisconnect:
            print(f"{websocket.client} closed")
            now_in.remove(websocket)
            enter_info[1]-=1
            try:
                await websocket.close()
            except :
                pass
            print("????")
            if(len(Q)):
                websocket = Q.popleft()
                now_in.add(websocket)
                enter_info[1]+=1
            return



async def send_queue_size():
    global Q
    while True:
        await asyncio.sleep(5)  # 5초마다 실행
        while(enter_info[1]<enter_info[0]):
            if len(Q):
                now_in.add(Q.popleft())
                enter_info[1]+=1

        idx=0
        it = Q.__iter__()
        next_Q = deque()
        while True:
            try:
                sw=next(it)
                try:
                    sw.send_text(f"waiting : {idx}")
                    idx+=1
                    Q.append(sw)
                except:
                    sw.close()

            except:
                break
        Q=next_Q