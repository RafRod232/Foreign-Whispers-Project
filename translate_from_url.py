from download import download_from_url
from translate import translate_text, translate_captions_file, translate_captions_folder
from speech import text_to_speech_audio
from whisper_model import generate_captions
import sys
import os
import pyttsx3

if len(sys.argv) <= 3:
	print("Misisng arguments")
	sys.exit()

url = sys.argv[1]
og_lang = sys.argv[2]
target_lang = sys.argv[3]

# download youtube video
video_path, caption_path, title = download_from_url(url)

# translate text
# translated_text = translate_captions_file(caption_path, og_lang, target_lang)
# print(f'Translated text from {og_lang} to {target_lang}:\n{translated_text}')

print("Generating Captions")
print(video_path)
print(f'audio\\{title}.wav')
text = generate_captions(video_path, f'audio\\{title}.wav')

print("Translating Captions")
translated_text = translate_text(text, og_lang, target_lang)
print(f'Translated text from {og_lang} to {target_lang}:\n{translated_text}')

print("Generating Transalted Audio")
engine = pyttsx3.init()
engine.setProperty('voice', "french")

engine.setProperty('rate', 150)
engine.setProperty('volume', 1)  
engine.save_to_file(translated_text, f"trans_audio\\{title}.mp3")
engine.runAndWait()

print("Done!")