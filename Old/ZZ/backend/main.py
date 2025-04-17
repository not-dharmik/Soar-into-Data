# import csv
# import os
# from fastapi import FastAPI
# from tsp_solver import get_static_route, get_dynamic_route
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # Allow local frontend to connect
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # For development only
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class AddressRequest(BaseModel):
#     addresses: list[str]
#     start: str

# @app.get("/static-route")
# def static_route():
#     result = get_static_route()
#     return result


# @app.post("/dynamic-route")
# def dynamic_route(payload: AddressRequest):
#     return get_dynamic_route(payload.addresses, payload.start)


import csv
import os
from fastapi import FastAPI
from tsp_solver import get_static_route, get_dynamic_route
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow local frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AddressRequest(BaseModel):
    addresses: list[str]
    start: str

@app.get("/static-route")
def static_route():
    result = get_static_route()
    print("Printing points in Sequence:")
    i=1
    for point in result:
        print(f"{i}. {point}")
        i+=1
    return result


@app.post("/dynamic-route")
def dynamic_route(payload: AddressRequest):
    return get_dynamic_route(payload.addresses, payload.start)


