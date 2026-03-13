from fastapi import FastAPI
import uvicorn
import sheets 
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

PATH = Path(__file__).resolve().parent

HTML_RESPONSE = PATH / 'Response' / 'index.html'

@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse(path=HTML_RESPONSE)






if __name__ == "__main__":
    uvicorn.run(app,port=8000)