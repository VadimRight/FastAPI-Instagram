from fastapi import FastAPI

app = FastAPI(
    title='Image Editor'
)


@app.get("/")
def get_hello():
    return {'Hello': 'World'}
