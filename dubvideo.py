from moviepy import VideoFileClip, AudioFileClip
import os

def merge_audio_with_video(original_video_path, dubbed_audio_path, output_dir, output_filename):
    # Ensure filename ends with .mp4
    if not output_filename.lower().endswith(".mp4"):
        output_filename += ".mp4"

    # Full output path
    output_video_path = os.path.join(output_dir, output_filename)

    # Load original video and dubbed audio
    video = VideoFileClip(original_video_path)
    dubbed_audio = AudioFileClip(dubbed_audio_path)

    # Replace original audio with dubbed audio
    video_with_dubbed_audio = video.with_audio(dubbed_audio)

    # Export the final video
    video_with_dubbed_audio.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    print(f"✅ Merged video saved to: {output_video_path}")

# if __name__ == "__main__":
#     original_video_path = input("Enter the path to the original video file: ").strip()
#     dubbed_audio_path = input("Enter the path to the dubbed audio file (e.g. 'dubbed_es.mp3'): ").strip()
#     output_dir = input("Enter the directory to save the dubbed video: ").strip()
#     output_filename = input("Enter the output video file name (e.g. 'dubbed_output.mp4'): ").strip()

#     merge_audio_with_video(original_video_path, dubbed_audio_path, output_dir, output_filename)
