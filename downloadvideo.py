import yt_dlp
import os

def download_youtube_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        'quiet': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

# # Example usage:
# if __name__ == "__main__":
#     url = input("Enter YouTube video URL: ").strip()
#     save_dir = input("Enter save directory (e.g., /Users/adityapatane/Desktop): ").strip()
#     file_name = input("Enter desired file name (e.g., myvideo.mp4): ").strip()

#     # Ensure directory exists
#     os.makedirs(save_dir, exist_ok=True)

#     # Construct full output path
#     output_path = os.path.join(save_dir, file_name)

#     video_path = download_youtube_video(url, output_path)
#     print(f"\n✅ Video downloaded to: {video_path}")

