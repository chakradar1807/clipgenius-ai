import subprocess
import uuid
import os

DOWNLOAD_DIR = "downloads"
OUTPUT_DIR = "outputs"

# Safe folder creation (fix FileExistsError)
if not os.path.isdir(DOWNLOAD_DIR):
    if os.path.exists(DOWNLOAD_DIR):
        os.remove(DOWNLOAD_DIR)
    os.mkdir(DOWNLOAD_DIR)

if not os.path.isdir(OUTPUT_DIR):
    if os.path.exists(OUTPUT_DIR):
        os.remove(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)


def download_video(url):
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    command = [
        "yt-dlp",
        "-f", "mp4",
        "-o", filepath,
        url
    ]

    print("⬇️ Downloading video...")

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=300   # ⏱️ prevent hanging
    )

    if result.returncode != 0:
        print("❌ yt-dlp error:", result.stderr)
        raise Exception("Video download failed")

    print("✅ Download complete")
    return filepath


def cut_clip(input_file, start, end, index):
    output = os.path.join(OUTPUT_DIR, f"clip_{index}.mp4")

    duration = end - start

    command = [
       "./ffmpeg",
        "-y",
        "-ss", str(start),
        "-i", input_file,
        "-t", str(duration),
        "-vf", "crop=ih*9/16:ih,scale=720:1280",
        "-c:v", "libx264",
"-c:a", "aac",
"-strict", "experimental",
        output
    ]

    print(f"✂️ Creating clip {index}...")

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=300   # ⏱️ prevent hanging
    )

    if result.returncode != 0:
        print("❌ FFmpeg error:", result.stderr)
        raise Exception("Clip creation failed")

    print(f"✅ Clip {index} done")
    return output