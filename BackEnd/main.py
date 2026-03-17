from fastapi import FastAPI
import uvicorn
from routes.servidoresNovos import router
from pathlib import Path
from fastapi.responses import FileResponse


app = FastAPI(title="Server lister GPCIT")

app.include_router(router)

PATH = Path(__file__).resolve().parent

HTML_RESPONSE = PATH / 'templates' / 'root' / 'index.html'

@router.get("/", response_class=FileResponse)
async def root():
    return FileResponse(path=HTML_RESPONSE)


if __name__ == "__main__":
    uvicorn.run("main:app",port=8000, reload=True)