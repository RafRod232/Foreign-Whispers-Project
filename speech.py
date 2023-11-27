import os
import pyttsx3

def text_to_speech_audio(directory_path, language, output_folder):
    engine = pyttsx3.init()
    engine.setProperty('voice', language)
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            txt_file_path = os.path.join(directory_path, filename)
            with open(txt_file_path, 'r') as file:
                text = file.read()
                #print(text)
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1)  
            output_audio_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".mp3")
            #print(output_audio_path)
            engine.save_to_file(text, f'trans_audio/{filename}.mp3')
            engine.runAndWait()

txt_path = "french_captions"
trans_lang = "french"
output_path = "trans_audio"
text_to_speech_audio(txt_path, trans_lang, output_path)