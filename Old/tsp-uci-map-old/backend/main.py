from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from tsp_solver import get_static_route, get_dynamic_route
from pydantic import BaseModel

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class AddressInput(BaseModel):
    addresses: list[str]

@app.get("/static-route")
def static_route():
    return get_static_route()

@app.post("/dynamic-route")
def dynamic_route(payload: AddressInput):
    return get_dynamic_route(payload.addresses)
