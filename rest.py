import time
from fastapi import FastAPI, File, Form
from fastapi import HTTPException, UploadFile, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI(title="Demo REST Server")


class Item(BaseModel):
    name: str
    price: float
    quantity: int


@app.get("/hello")
async def hello() -> Response:
    return JSONResponse({"message": "Hello, World"})


@app.get("/get_user/{user_id}")
async def get_user(user_id: int) -> Response:
    return JSONResponse({"message": f"You requested data of {user_id}"})


@app.put("/update/{item_id}")
async def update_item(item_id: int, item: Item) -> Response:
    return JSONResponse({
        "item_id": item_id,
        "item_name": item.name,
        "item_price": item.price,
        "item_quantity": item.quantity
    })


@app.post("/upload/")
async def upload_file(file_id: int = Form(), file: UploadFile = File()) -> Response:
    return JSONResponse({
        "file_id": file_id,
        "file_name": file.filename,
        "file_type": file.content_type
    })


@app.get("/view_request_info")
async def view_request_info(request: Request) -> Response:
    return JSONResponse({k: v for k, v in request.headers.items()})


@app.middleware("http")
async def check_token(request: Request, _next) -> Response:
    if request.headers["apiKey"] != "this_is_my_key":
        raise HTTPException(status_code=status.WS_1008_POLICY_VIOLATION, detail="apiKey mismatched")

    start_time = time.time()
    response: Response = await _next(request)
    response.headers["X-Process-Time"] = str(time.time() - start_time)

    return response
