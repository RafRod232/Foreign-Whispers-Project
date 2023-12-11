import os
from moviepy.editor import VideoFileClip
import whisper

model = whisper.load_model("base")

# generate captions for single video file
def generate_captions(video_file_path, audio_file_path):
	# separate audio file
	video = VideoFileClip(video_file_path)
	video.audio.write_audiofile(audio_file_path, codec='pcm_s16le')

	# use whisper model to generate captions on audio file
	result = model.transcribe(audio_file_path)

	return result["text"]

# generate captions for all video files in a folder and output to text files in captions folder
def generate_captions_folders(video_folder_path, audio_folder_path, caption_folder_path):
    video_files = [f for f in os.listdir(video_folder_path) if f.endswith(".3gpp")]
    for video_file in video_files:
        video_file_path = os.path.join(video_folder_path, video_file)
        audio_file = os.path.join(audio_folder_path, os.path.splitext(video_file)[0] + ".wav")
        caption_file = os.path.join(caption_folder_path, os.path.splitext(video_file)[0] + ".txt")

        video = VideoFileClip(video_file_path)
        video.audio.write_audiofile(audio_file)

        result = model.transcribe(audio_file)
        
        with open(caption_file, "w") as file:
        	file.write(result["text"])

        print(f"Transcription for {video_file}: {result['text']}")

# generate_captions("D:\\github-repos\\Foreign-Whispers-Project\\videos\\Bill Gates The 2021 60 Minutes interview.3gpp", "audio\\test.wav")
# generate_captions_folders("videos", "audio", "whisper_captions")