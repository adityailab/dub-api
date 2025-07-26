# main.py

import os
from downloadvideo import download_youtube_video
from transcript import transcribe_video_to_srt_and_bgm
from translate import translate_srt
from dubaudio import generate_and_combine_audio
from dubvideo import merge_audio_with_video

def main():
    # Step 1: Download YouTube Video
    url = input("Enter YouTube video URL: ").strip()
    save_dir = input("Enter directory to save the video: ").strip()
    file_name = input("Enter desired video filename (e.g., myvideo.mp4): ").strip()
    if not os.path.splitext(file_name)[1]:
        file_name += ".mp4"
    os.makedirs(save_dir, exist_ok=True)
    video_path = os.path.join(save_dir, file_name)

    print("\n📥 Downloading video...")
    download_youtube_video(url, video_path)
    print(f"✅ Video saved at: {video_path}")

    # Step 2: Extract Audio, Transcribe, Save SRT & Separate BGM
    audio_name = input("Enter audio filename (e.g., audio.wav): ").strip()
    if not os.path.splitext(audio_name)[1]:
        audio_name += ".wav"
    audio_path = os.path.join(save_dir, audio_name)

    srt_name = input("Enter subtitle filename (e.g., subtitles.srt): ").strip()
    if not os.path.splitext(srt_name)[1]:
        srt_name += ".srt"
    srt_path = os.path.join(save_dir, srt_name)

    model_size = input("Enter Whisper model size (tiny, base, small, medium, large) [default=small]: ").strip() or "small"

    print("\n🧠 Processing video for transcription and BGM separation...")
    bgm_output_subdir = input("Enter a folder name to save BGM separation (e.g., bgm_outputs): ").strip()
    bgm_path = os.path.join(save_dir, bgm_output_subdir)
    os.makedirs(bgm_path, exist_ok=True)


    transcribe_video_to_srt_and_bgm(
        video_path=video_path,
        model_size=model_size,
        audio_path=audio_path,
        srt_path=srt_path,
        bgm_output_dir=bgm_path
    )

    # Step 3: Translate subtitles
    translated_srt_path = srt_path
    translate = input("\n🌍 Do you want to translate subtitles? (yes/no): ").strip().lower()
    if translate in ["yes", "y"]:
        target_lang = input("Enter target language code (e.g., 'es' for Spanish): ").strip()
        translated_filename = input("Enter output filename for translated .srt (e.g., translated.srt): ").strip()
        if not os.path.splitext(translated_filename)[1]:
            translated_filename += ".srt"
        translated_srt_path = os.path.join(save_dir, translated_filename)

        translate_srt(
            input_srt=srt_path,
            output_dir=save_dir,
            output_filename=translated_filename,
            target_lang=target_lang
        )

    # Step 4: Generate dubbed audio
    dubbed_audio_path = ""
    do_dub = input("\n🔊 Do you want to generate dubbed audio from the subtitles? (yes/no): ").strip().lower()
    if do_dub in ["yes", "y"]:
        dub_lang = input("Enter language code for dubbing (e.g., 'es'): ").strip()
        dub_audio_name = input("Enter output audio filename (e.g., dubbed_audio.mp3): ").strip()
        if not os.path.splitext(dub_audio_name)[1]:
            dub_audio_name += ".mp3"
        dubbed_audio_path = os.path.join(save_dir, dub_audio_name)

        generate_and_combine_audio(
            input_srt=translated_srt_path,
            output_audio_path=save_dir,
            output_file_name=dub_audio_name,
            lang=dub_lang
        )

    # Step 5: Merge dubbed audio with video
    if dubbed_audio_path:
        do_merge = input("\n🎬 Do you want to merge dubbed audio with the original video? (yes/no): ").strip().lower()
        if do_merge in ["yes", "y"]:
            output_filename = input("Enter the output video filename (e.g., final_video.mp4): ").strip()
            if not os.path.splitext(output_filename)[1]:
                output_filename += ".mp4"

            merge_audio_with_video(
                original_video_path=video_path,
                dubbed_audio_path=dubbed_audio_path,
                output_dir=save_dir,
                output_filename=output_filename
            )

if __name__ == "__main__":
    main()
