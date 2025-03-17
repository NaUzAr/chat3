# app/media_service.py

import os
import uuid
from fastapi import UploadFile, HTTPException
import aiofiles
import shutil

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def save_media(file: UploadFile) -> str:
    try:
        # Buat direktori uploads jika belum ada
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # Generate nama file yang unik
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_extension}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        # Simpan file menggunakan shutil (lebih sederhana)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Kembalikan URL relatif untuk akses file
        return f"/media/{filename}"
    except Exception as e:
        print(f"Error saving media: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")