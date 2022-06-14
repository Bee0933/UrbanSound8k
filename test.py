# import required modules
import os
import config
from pydub import AudioSegment
  
# assign files
input_file = os.path.join(config.UPLOAD_PATH, 't.mp3')
filename, ext = os.path.splitext(input_file)
print(ext)
output_file = os.path.join(config.UPLOAD_PATH, 'result.wav')
  
# convert mp3 file to wav file
# sound = AudioSegment.from_mp3(input_file)
# sound.export(output_file, format="wav")

def convert_mp3_to_wave(input_file,output_file):
      sound = AudioSegment.from_mp3(input_file)
      sound.export(output_file, format="wav")