from fastapi import FastAPI
import numpy
from math import pi
app = FastAPI()
bs5 = bs4.BeautifulSoup()
print("Hello World")
print(pi)
@app.get("/")
def root():
    return {
        "status": 200,
        "details": "ok",
        "result": "working"
    }