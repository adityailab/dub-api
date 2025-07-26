from gtts import gTTS
import os
import srt
from pydub import AudioSegment
from datetime import timedelta

def generate_and_combine_audio(input_srt, output_audio_path, output_file_name, lang='es'):
    # Read subtitles
    with open(input_srt, 'r', encoding='utf-8') as f:
        subtitles = list(srt.parse(f.read()))

    # Determine total duration
    total_duration = int(subtitles[-1].end.total_seconds() * 1000)
    combined = AudioSegment.silent(duration=total_duration)

    for i, sub in enumerate(subtitles):
        # Generate TTS
        tts = gTTS(text=sub.content, lang=lang)
        temp_path = f"clip_{i:04d}.mp3"
        tts.save(temp_path)

        # Load clip and get timings
        clip = AudioSegment.from_file(temp_path)
        start_ms = int(sub.start.total_seconds() * 1000)
        end_ms = int(sub.end.total_seconds() * 1000)
        max_duration = end_ms - start_ms

        # Truncate clip if too long
        if len(clip) > max_duration:
            clip = clip[:max_duration]

        # Overlay TTS onto the silent base
        combined = combined.overlay(clip, position=start_ms)

        # Clean up
        os.remove(temp_path)

    # Export
    final_path = os.path.join(output_audio_path, output_file_name)
    combined.export(final_path, format="mp3")
    print(f"✅ Dubbed audio saved to: {final_path}")


# # Example usage
# if __name__ == "__main__":
#     input_srt = input("Enter the path to translated .srt: ").strip()
#     output_audio_path = input("Enter folder path to save dubbed audio: ").strip()
#     output_file_name = input("Enter output audio file name (with .mp3 extension): ").strip()
#     if not os.path.splitext( output_file_name)[1]:
#          output_file_name += ".mp3"
#     lang = input("Enter language code (e.g. 'es'): ").strip()

#     generate_and_combine_audio(input_srt, output_audio_path, output_file_name, lang)
