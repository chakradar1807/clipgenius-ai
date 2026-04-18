from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from video_utils import download_video, cut_clip

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    url: str


@app.post("/generate-ai-reels")
def generate_ai_reels(req: RequestData):
    try:
        print("🚀 START")

        # STEP 1: download
        video = download_video(req.url)
        print("📁 Video:", video)

        if not os.path.exists(video):
            return {"status": "error", "message": "Video not downloaded"}

        # STEP 2: create ONLY ONE clip (test fix)
        start = 5
        end = 25

        clip = cut_clip(video, start, end, 1)

        print("📁 Clip:", clip)

        if not os.path.exists(clip):
            return {"status": "error", "message": "Clip not created"}

        print("✅ SUCCESS")

        return {
            "status": "success",
            "clips": [clip]
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {"status": "error", "message": str(e)}


@app.get("/download")
def download(file: str):
    if not os.path.exists(file):
        return {"error": "File not found"}

    return FileResponse(
        path=file,
        media_type="video/mp4",
        filename="reel.mp4"
    )