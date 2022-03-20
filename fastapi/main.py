from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

# 启动：uvicorn main:app --reload
# main：main.py 文件（一个 Python "模块"）。
# app：在 main.py 文件中通过 app = FastAPI() 创建的对象。
# --reload：让服务器在更新代码后重新启动。仅在开发时使用该选项。
app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
