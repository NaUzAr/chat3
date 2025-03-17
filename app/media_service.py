import os
import uuid
from fastapi import UploadFile, HTTPException
import aiofiles

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def save_media(file: UploadFile) -> str:
    # Buat direktori uploads jika belum ada
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Validasi ukuran file
    file_size = 0
    async for chunk in file.file:
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
    
    # Reset posisi file
    await file.seek(0)
    
    # Generate nama file yang unik
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{file_extension}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    try:
        # Simpan file secara asinkron
        async with aiofiles.open(filepath, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
    except Exception as e:
        # Jika terjadi kesalahan saat menyimpan file
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Kembalikan URL relatif untuk akses file
    return f"/media/{filename}"
