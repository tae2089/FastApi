from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/")
async def root():
    return {"message": "Hello World"}


#Path Parameter example
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

#Query Parameter
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

#Request Body
@app.post("/items2/")
async def create_item(item: Item):
    return item

#Order matters
#경로가 동일한 함수가 두개 이상 존재할 경우 위에 선언된 메소드부터 검색이 됨
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}
#Order matters
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
