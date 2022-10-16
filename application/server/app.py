from fastapi import FastAPI
from API import batata

app = FastAPI()


@app.get("/", tags=["Root"])
async def welcome_msg():
    return {"message": "Welcome to this fantastic app!"}

@app.get("/robo", tags=["Root"])
async def about_us():
    return {"message": "Bem vindo a este robo! Feito e idealizado por Filipe, Iago e Igor"}

@app.get("/batata", tags=["Root"], response_description="Example description")
async def Example_APIs():
    return batata.Batata()