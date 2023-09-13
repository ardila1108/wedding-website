from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def healthcheck():
    return {"status": "Online"}


@app.get("/info")
def get_company_profile():
    return {"status": "FUCK YEAH"}
