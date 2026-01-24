from fastapi import APIRouter, File, UploadFile
import shutil

from fastapi.responses import FileResponse

router = APIRouter(prefix="/file",tags=['file'])


@router.post('/upload')
async def upload_simple_file(file: bytes =  File(...)):
    content = file.decode('utf-8')
    splitted_lines = content.split('\n')
    return {"result": splitted_lines}

@router.post('/uploadfile')
async def upload_modern_file(file: UploadFile = File(...)):
    path = f"files/{file.filename}"
    
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "fileName": path,
        "fileType": file.content_type
    }
    
@router.get('/download/{name}', response_class=FileResponse)
async def download_file(name: str):
    path = f"files/{name}"
    return path