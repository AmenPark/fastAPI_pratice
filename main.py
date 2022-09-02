from fastapi import FastAPI

app = FastAPI()

test_list = [0] * 10

@app.get("/")               # 데코레이터.
async def root():           # async는 비동기 선언.
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id : int):
    if item_id >= 10 or item_id < 0:
        return {"message" : "ERROR404"}
    else:
        test_list[item_id] += 1
    return {"item_id:": test_list[item_id]}