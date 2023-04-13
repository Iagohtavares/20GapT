from fastapi import FastAPI, Request
from API import data
from API import operations

app = FastAPI()


@app.get("/", tags=["Root"])
async def welcome_msg():
    return {"message": "Welcome to this fantastic app! Made by Filipe, Iago e Igor"}


@app.get("/data", tags=["Root"], response_description="Get the values of MetaTrader")
async def datas():
    return data.get_last_close_candle()


@app.get("/buy", tags=["Root"], response_description="Buy")
async def datas():
    return operations.makes_purchase()
