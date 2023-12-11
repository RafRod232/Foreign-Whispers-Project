import streamlit as st
from pytube import YouTube
from pytube import Caption
import os
from moviepy.editor import VideoFileClip
import whisper
import argostranslate.package
import argostranslate.translate
import pyttsx3

from download import download_from_url
from translate import translate_text, translate_captions_file, translate_captions_folder

# Streamlit app UI
st.title("YouTube Video Downloader with Captions")

# Get YouTube video URL from user input
video_url = st.text_input("Enter YouTube Video URL:")

original_language =  st.text_input("Enter the input language")
target_language =  st.text_input("Enter the desired language")

# Button to trigger video download and caption generation
if st.button("Download Video and Generate Captions"):
    try:
        # Download video using Pytube
        video = YouTube(video_url)
        video_title = video.title
        video_stream = video.streams.filter(file_extension="mp4").first()
        video_path = os.path.join(video_output_folder, f"{video_title}.mp4")
        video_stream.download(output_path=video_output_folder)


        st.success("Download video successfully!")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

    model = whisper.load_model("base")
    def generate_captions_folders(video_folder_path, audio_folder_path, caption_folder_path):
        video_files = [f for f in os.listdir(video_folder_path) if f.endswith(".mp4")]
        for video_file in video_files:
            video_file_path = os.path.join(video_folder_path, video_file)
            audio_file = os.path.join(audio_folder_path, os.path.splitext(video_file)[0] + ".wav")
            caption_file = os.path.join(caption_folder_path, os.path.splitext(video_file)[0] + ".txt")

            video = VideoFileClip(video_file_path)
            video.audio.write_audiofile(audio_file)

            result = model.transcribe(audio_file)
            
            with open(caption_file, "w") as file:
                file.write(result["text"])
            
            #print(f"Transcription for {video_file}: {result['text']}")

    generate_captions_folders(video_output_folder, audio_output_folder, captions_output_folder)
    def translate_text(text, from_code, to_code):
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        package_to_install = next(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
            )
        )
        argostranslate.package.install_from_path(package_to_install.download())
        return argostranslate.translate.translate(text, from_code, to_code)

    def translate_captions_file(file_path, from_code, to_code):
        captions_file = open(file_path, "r")
        captions_text = captions_file.read()
        captions_file.close()
        return translate_text(captions_text, from_code, to_code)

    def translate_captions_folder(folder_path, from_code, to_code, output_folder):
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                translated_text = translate_captions_file(file_path, from_code, to_code)
                #translated_texts[filename] = translated_text
                output_file_path = os.path.join(output_folder, f"{filename.split('.')[0]}_translated.txt")
                with open(output_file_path, "w") as output_file:
                    output_file.write(translated_text)
                    
    translate_captions_folder(captions_output_folder, "en",trans_lang_short, trans_text_folder)

    def text_to_speech_audio(directory_path, language, output_folder):
        # ----- #
        # it throws a 1 ReferenceError: weakly-referenced object no longer exists
        # ----- #
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
                engine.save_to_file(text, f'{output_folder}/{filename}.mp3')
                engine.runAndWait()
    text_to_speech_audio(trans_text_folder, trans_lang_full, trans_audio_folder)
    st.header("Captions from Video")
    # ----- #
    # Does not recognize file at that location says it is nonexistenct 
    # ----- #
    captionfullpath = os.path.join(captions_output_folder,os.listdir(captions_output_folder)[0])
    with open(captionfullpath, 'r') as captions_file:
        original_captions = captions_file.read()
        st.text(original_captions)
    transtextfullpath = os.path.join(trans_text_folder,os.listdir(trans_text_folder)[0])
    st.header("Translated Captions from Video")
    with open(transtextfullpath, 'r') as translated_captions_file:
        translated_captions = translated_captions_file.read()
        st.text(translated_captions)

        # Play audio
    transaudiofullpath = os.path.join(trans_audio_folder,os.listdir(trans_audio_folder)[0])
    st.audio(transaudiofullpath, format='audio/mp3')

    st.success("Text and Audio Translation completed!")