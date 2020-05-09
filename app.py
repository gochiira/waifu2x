from fastapi import FastAPI
from uuid import uuid4
from time import time
import uvicorn
import subprocess
import tempfile
import requests
import os
import shutil

app = FastAPI()


@app.get("/")
async def root():
    return {"status": 200, "message": "Server is running."}


@app.post('/predict')
async def predictByDeepDanbooru():
    return {"message": "Not implemented"}


@app.get('/zoom')
async def zoomByWaifu2xConverterCpp(url: str = None, size: float = 2.0):
    if not url:
        return {"message": "Need url"}
    if not url.startswith('https://cdn.gochiusa.team/illusts/orig/'):
        return {"message": "Invalid url"}
    if size < 1.0 or size > 10.0:
        return {"message": "Invalid size"}
    with tempfile.TemporaryDirectory() as tempPath:
        resp = requests.get(url)
        if resp.status_code != 200:
            return {"message": "Invalid url"}
        uid = str(uuid4()).replace('-', '')
        ext = url.split('.')[-1]
        imgPath = f'{tempPath}\\{uid}.{ext}'
        outPath = f'{tempPath}\\{uid}_waifu{size}x.{ext}'
        with open(imgPath, 'wb') as f:
            f.write(resp.content)
        convertStart = time()
        subprocess.run(
            f'./waifu2x-caffe/waifu2x-caffe-cui.exe -i {imgPath} -o {outPath}',
            shell=True
        )
        convertEnd = time()
        processTime = int(convertEnd - convertStart)
        finalPath = f'D:\\Documents\\Gits\\Gochiusa_Illustration\\Waifu2x\\waifu-{size}x.{uid}.{ext}'
        shutil.move(outPath, finalPath)
    return {"message": f"Generated in {processTime} seconds"}

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
