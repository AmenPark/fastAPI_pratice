from fastapi import FastAPI
from typing import Union, List
from pydantic import BaseModel, HttpUrl

app = FastAPI()

test_list = [0] * 10

'''
uvicorn main:app --reload를 통해서 실행.

기본 페이지 127.0.0.1:8000/ 는 @app.get("/")으로 표현.
경로는 이후 이 뒤에 붙임. @app.get("/data/")이런식
{}을 통해서 fstring처럼 인자 표현이 가능. 타입 지정을 통해 정수/문자열 등 고정 가능.
앞부터 체크하므로 /data/me 랑 /data/{string_data}/가 둘 다 존재할경우 순서에 따라 /data/me의 작동이 달라짐.
쿼리는 주소에서 .../?a=0&b=1... 꼴로 표현된다. 이를 받기 위해서는 함수에 매개변수로 전달된다.
경로 매개변수 - 데코레이터. 쿼리 매개변수 - 함수 매개변수.
**kwds 를 통해서 쿼리를 무제한으로 받을 수 있다. 처리만 안하면 에러는 없다?

body에 어떤 값이 있는 경우. request body는 json식.
이것에 대한 object를 class로 정의해서 하도록 한다.
pydantic에서 BaseModel을 사용하는데, 이는 타입 검증을 위한 것. type hint를 통해서 변수 데이터 유형을 정한다.
constrained types를 통해서 constr(min_length = 2, max_length=10)과 같은 방식으로 제한 가능.
Strict를 통한 엄격한 검사도 가능.
이 body는 get요청에서의 쿼리처럼 매개변수로 전달받음.
보통은 post요청에서 쓰임. put도 마찬가지. 

Union[Class_Item, None]을 통해서 타입을 A 또는 B 형식으로 제한 가능.

fastAPI 에서 Query, Path는 각각 쿼리/패스의 검증에 쓰인다.
Query : fastapi.Query를 import.
    def fun(q) 에서 q: Union(str, None) = Query(default = None, max_length = 50)처럼 사용.
    매개변수란에 ?뒤의 쿼리값에 대한 제한이 가능해진다.
Path : Query와 기본적으로 매우 동일한 효과를 지닌다. 그러나 데코레이터에서 {item_id}와 같은식의 값을 넣어준다.
즉, Query, Path 둘 다 매개변수로 함수에 주어지는데 데코레이터에 표현되느냐의 차이가 있는 것이다.

Body는 말 그대로 body에 관하여 Query, Path처럼 매개변수들에서 쓸 수 있다. 차이점은 post, put류에서 쓰인다?
코드상으로 Body로 여럿 줄 수 있다. 기능은 하지만 글쎄...?

Query, Path, Body 등과 pydantic.Field는 거의 동일한 역할이 가능하다.

typing에서 List를 가져와서 하나의 타입으로만 값을 갖는 리스트 선언이 가능하다.
동적 언어인 파이썬을 정적으로 바꿔 오류를 줄여주는 역할을 할 것으로 보인다.
set도 비슷하게 가능하며, dict는 key-value 각각 타입 지정이 가능하다.

비슷한 예시로 pydantic에서 HttpUrl타입을 가져올 수 있다. 이 검증은 대표적으로 이미지에 좋을 것이다.

클래스 내부에 config 클래스를 정의하고, schema_extra를 이용해서 예시를 만들 수 있다.
이 예시는 JSON 스키마로서 API 요청 docs에 표시된다.

쿠키 사용은 fastapi.Cookie를 사용한다. 쿼리매개변수와 사용법은 동일한데 매개변수로 줄 때에 Cookie로 줘야만 한다.
사용법은 def func1 (CK : Union[str, None] = Cookie(default = None)) 꼴로 사용.

헤더 또한 마찬가지로 사용 가능하다. Header로 바뀐다는 점만 다르다. 거기에 추가 기능이 있다.
헤더는 -(하이픈)문자를 통해서 구분하는데 파이썬에서 _와 자동 호환하는 기능이 존재한다. 파이썬 변수명은 a-b는 될 수 없어서.
이 기능은 Header의 매개변수 convert_underscores가 디폴트 True값일때 작동하므로 False로 바꿔 끌 수 있다.
여러 헤더라면 리스트 형태로 받는식으로 해결가능.

response도 모델을 이용해서 가능. 이는 데코레이터 경로로 들어간다.
@app.post("/items/", response_model = Item)
이라고 하면 Item class가 response_model이 되는 것이다.
모델에 맞지 않는 출력을 할 경우 적당히 없앨 attribute는 알아서 제거해주는데 빈건 어떻게 채울지는 모르겠다.
None으로 채워주나? 그러기에는 type까지 제한 줘서 빡세게 할텐데..
모델 수가 제한되어 있고, 모델의 일부분만 넘겨 줄 때는 response_model_exclude, response_model_include를 쓴다.
사용법은 response_model과 마찬가지로 데코레이터 부분에 인자로 넘겨진다.
기본적으로는 response_model_exclude = {"tax", "tags"}와 같이 set로 쓰이며, 리스트로 넘겨줘도 set으로 자동변환된다.
각각 이것만, 이걸 제외하고? 정도로 쓰인다.

데코레이터에 응답코드 매개변수를 넣을 수 있다. status_code = 201과 같은 방식.
HTTP 상태코드를 받는다. 응답에서 해당 상태코드를 반환한다. 문서화에 추가한다.

'''

class Item(BaseModel):
    name : str
    description : Union[str, None] = None
    price : float
    tax : Union[float, None] = None
    tags : List[str] = []

    class config:
        schema_extra = {
            "example" : {
                "name" : "golden sword",
                "description" : "T1 sword",
                "price" : 35.4,
                "tax" : 3.5,
                "tags" : ["T1", "oneHandWeapone", "light"],
            }
        }

class Image(BaseModel):
    url : HttpUrl
    name : str


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