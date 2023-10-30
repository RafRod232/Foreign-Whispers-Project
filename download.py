import pytube
import os
from pytube import YouTube
from pytube import Channel
from pytube import Playlist

# sanitizes file names for windows files
def sanitize_filename(filename):
    # List of characters that are invalid in Windows filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

# need to use fix from pr #1409 for channels
# apply here: "C:\Python311\Lib\site-packages\pytube\contrib\channel.py"
# need to use fix from pr #1085 for captions
# apply here: "C:\Python311\Lib\site-packages\pytube\captions.py"
p = Playlist('https://www.youtube.com/playlist?list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL')
current_directory = os.path.dirname(os.path.realpath(__file__))
videos_output_directory = os.path.join(current_directory, 'videos')
captions_output_directory = os.path.join(current_directory, 'captions')

print(f'Downloading videos from: {p.title}')

count = 10
i = 0
k = 0

while i < len(p.videos) and k < count:
	# have to use this method before accessing other properties like captions
	# https://github.com/pytube/pytube/issues/1674#issuecomment-1706105785
	# save videos
	video = p.videos[i]
	print(f'Checking: {video.title}')
	if video.age_restricted == True:
		i += 1
		print('Age restricted')
		continue
	try:
		video.bypass_age_gate()
		print('Not age restriced')
		caption = video.captions['en']
		print(caption)
		caption_content = caption.generate_srt_captions()
		caption_filename = f"{sanitize_filename(video.title)}.srt"
		caption_path = os.path.join(captions_output_directory, caption_filename)
		with open(caption_path, 'w', encoding='utf-8') as file:
			file.write(caption_content)

		video.streams.first().download(output_path=videos_output_directory)
		k += 1
		i += 1
	except:
		print('No captions')
		i += 1
		continue