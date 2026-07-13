from fastapi import FastAPI

app = FastAPI();

@app.get("/")
def root():
    return {"status":"online", "messege":"backend is runing"}

@app.get("/{item_id}")
def return_item(item_id: int, q: str | None = None):
    return {"item_id": item_id , "query_parameter": q}
