from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": 'Hello Jeff with simple quotes'}


