from deep_translator import GoogleTranslator
import re
import os

def translate_srt(input_srt, output_dir, output_filename, target_lang='es'):
    with open(input_srt, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r'\n\s*\n', content.strip())
    translated_blocks = []

    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            index = lines[0]
            timestamp = lines[1]
            text_lines = lines[2:]

            try:
                translated_text = "\n".join(
                    GoogleTranslator(source='auto', target=target_lang).translate(line)
                    for line in text_lines
                )
                translated_block = f"{index}\n{timestamp}\n{translated_text}"
                translated_blocks.append(translated_block)
            except Exception as e:
                print(f"⚠️ Translation failed for block {index}: {e}")
                translated_blocks.append(block)

    # Build full output path
    os.makedirs(output_dir, exist_ok=True)
    output_srt_path = os.path.join(output_dir, output_filename)

    with open(output_srt_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(translated_blocks))

    print(f"\n✅ Translated subtitles saved to: {output_srt_path}")


# # Example usage
# if __name__ == "__main__":
#     input_srt = input("Enter full path to input .srt file: ")
#     output_dir = input("Enter output directory path: ")
#     output_filename = input("Enter output .srt file name (e.g., translated.srt): ")
#     if not os.path.splitext( output_filename)[1]:
#          output_filename += ".srt"
#     target_lang = input("Enter target language code (e.g., 'es' for Spanish): ")

#     translate_srt(input_srt, output_dir, output_filename, target_lang)
