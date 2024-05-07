from fastapi import APIRouter 
from fastapi.responses import FileResponse


router = APIRouter()

@router.get("/download-txt")
async def download_txt_file():
    file_path = "./data/data.txt"
    return FileResponse(file_path, media_type='text/plain', filename="data.txt")
