from fastapi import FastAPI, Form   
from pydantic import BaseModel
import os
from downloadvideo import download_youtube_video
from transcript import transcribe_video_to_srt_and_bgm
from translate import translate_srt
from dubaudio import generate_and_combine_audio
from dubvideo import merge_audio_with_video

app = FastAPI()
@app.get("/")
def home():
    return {"message": "🎬 YouTube Video Dubbing API is running!"}


class VideoProcessRequest(BaseModel):
    url: str
    save_dir: str
    file_name: str
    audio_name: str
    srt_name: str
    model_size: str = "small"
    bgm_output_subdir: str
    translate: bool = False
    target_lang: str = ""
    translated_srt_name: str = ""
    do_dub: bool = False
    dub_lang: str = ""
    dub_audio_name: str = ""
    do_merge: bool = False
    final_video_name: str = ""

@app.post("/process/")
def process_video(req: VideoProcessRequest):
    os.makedirs(req.save_dir, exist_ok=True)
    video_path = os.path.join(req.save_dir, req.file_name)

    download_youtube_video(req.url, video_path)

    audio_path = os.path.join(req.save_dir, req.audio_name)
    srt_path = os.path.join(req.save_dir, req.srt_name)
    bgm_path = os.path.join(req.save_dir, req.bgm_output_subdir)
    os.makedirs(bgm_path, exist_ok=True)

    transcribe_video_to_srt_and_bgm(
        video_path=video_path,
        model_size=req.model_size,
        audio_path=audio_path,
        srt_path=srt_path,
        bgm_output_dir=bgm_path
    )

    translated_srt_path = srt_path
    if req.translate:
        translated_srt_path = os.path.join(req.save_dir, req.translated_srt_name)
        translate_srt(
            input_srt=srt_path,
            output_dir=req.save_dir,
            output_filename=req.translated_srt_name,
            target_lang=req.target_lang
        )

    dubbed_audio_path = ""
    if req.do_dub:
        dubbed_audio_path = os.path.join(req.save_dir, req.dub_audio_name)
        generate_and_combine_audio(
            input_srt=translated_srt_path,
            output_audio_path=req.save_dir,
            output_file_name=req.dub_audio_name,
            lang=req.dub_lang
        )

    if req.do_merge and dubbed_audio_path:
        merge_audio_with_video(
            original_video_path=video_path,
            dubbed_audio_path=dubbed_audio_path,
            output_dir=req.save_dir,
            output_filename=req.final_video_name
        )

    return {"status": "success", "video_path": video_path}
