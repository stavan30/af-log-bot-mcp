from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional, List, Union
from app.log_parser import search_logs

app = FastAPI()

class QueryRequest(BaseModel):
    username: Optional[str] = None
    resp_code: Optional[Union[int, List[int]]] = None
    keyword: Optional[str] = None
    last_n_minutes: Optional[int] = 10

@app.get("/")
def read_root():
    return {"message": "MCP Log Query Server is running."}

@app.post("/query")
def query_logs(request: QueryRequest):
    """
    Accepts a POST request with optional filters:
    - username
    - response code
    - keyword in message
    - last_n_minutes (defaults to 10)
    """
    results = search_logs(
        username=request.username,
        resp_code=request.resp_code,
        keyword=request.keyword,
        last_n_minutes=request.last_n_minutes
    )
    return {"results": results, "count": len(results)}
