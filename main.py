"""
FastAPI main file
"""

import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Assistant",
    description="A simple assistant to help you with your daily tasks",
    version="0.0.1",
)

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:8000",
    "localhost:8000",
    "http://localhost:8080",
    "localhost:8080",
    "http://localhost:5173",
    "localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

from sqlchain import SequentialChain
assistant = SequentialChain()

class Item(BaseModel):
    query : str


@app.get("/")
def read_root():
    return {"Hello": "Welcome to Assistant"}



@app.get("/get_dataset_lov")
def get_dataset_lov():
    return {"names": ["accs", "aps"]}


@app.post("/get_answer")
def get_answer(item: Item):
    return {"answer": assistant.get_agent_answer(item.query)}



# uvicorn main:app --reload --port 8000 