import whisper
from moviepy import VideoFileClip
import os
import subprocess

def extract_audio_from_video(video_path, audio_path="extracted_audio.wav"):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result

def save_transcription_as_srt(result, output_srt="subtitles.srt"):
    with open(output_srt, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"]):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            f.write(f"{i + 1}\n")
            f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
            f.write(f"{text}\n\n")

def format_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

import subprocess

def separate_bgm_with_demucs(audio_path, output_dir):
    print("Separating background music using Demucs...")
    command = [
        "demucs", "--two-stems=vocals", "-n", "htdemucs",
        "-o", output_dir, audio_path
    ]
    subprocess.run(command, check=True)
    print("BGM and vocals saved to:", output_dir)


def transcribe_video_to_srt_and_bgm(video_path, model_size, audio_path, srt_path, bgm_output_dir):
    print("Extracting audio from video...")
    audio_path = extract_audio_from_video(video_path, audio_path)
    print(f"Audio saved to: {audio_path}")

    print("Transcribing speech...")
    result = transcribe_audio(audio_path, model_size)

    print("Saving subtitles as SRT...")
    save_transcription_as_srt(result, srt_path)
    print(f"Subtitles saved to: {srt_path}")

    separate_bgm_with_demucs(audio_path, bgm_output_dir)
    print("BGM Done.")

# # Run as main script
# if __name__ == "__main__":
#     video_path = input("Enter path to the video file: ").strip()

#     audio_dir = input("Enter directory to save extracted audio (e.g., /Users/name/Desktop): ").strip()
#     audio_name = input("Enter audio filename (e.g., audio.wav): ").strip()
#     if not os.path.splitext(audio_name)[1]:
#         audio_name += ".wav"
#     audio_path = os.path.join(audio_dir, audio_name)

#     srt_dir = input("Enter directory to save subtitle file: ").strip()
#     srt_name = input("Enter subtitle filename (e.g., subtitles.srt): ").strip()
#     if not os.path.splitext(srt_name)[1]:
#         srt_name += ".srt"
#     srt_path = os.path.join(srt_dir, srt_name)

#     bgm_output_dir = audio_dir

#     model_size = input("Enter Whisper model size (tiny, base, small, medium, large) [default=small]: ").strip() or "small"

#     os.makedirs(audio_dir, exist_ok=True)
#     os.makedirs(srt_dir, exist_ok=True)
#     os.makedirs(bgm_output_dir, exist_ok=True)

#     transcribe_video_to_srt_and_bgm(
#         video_path=video_path,
#         model_size=model_size,
#         audio_path=audio_path,
#         srt_path=srt_path,
#         bgm_output_dir=bgm_output_dir
#     )
