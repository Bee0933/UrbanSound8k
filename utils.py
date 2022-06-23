from json import load
import os
import glob
import shutil
import config
import pickle as pkl
import librosa
import numpy as np
from pydub import AudioSegment
import tensorflow as tf
from tensorflow.keras.models import load_model 


import warnings
warnings.filterwarnings(action='ignore')

audio_folders = [ 'air_conditioner', 'car_horn', 
'children_playing', 'dog_bark', 'drilling', 
'engine_idling', 'gun_shot', 'jackhammer', 
'siren', 'street_music']

base_dir = 'dataset/'


# function to copy all audio files in the audio folders into a new folders defined by their unique class names
def arrange_files():
      folders = glob.glob(os.path.join(config.AUDIO_FILES_PATH, '*'))

      for fold in folders:
            files = glob.glob(os.path.join(fold, '*.wav'))

            for file in files:
                  # print(file)
                  class_id = audio_folders[int(os.path.basename(file).split('-')[1])]
                  if not os.path.isdir(base_dir + class_id): 
                        os.makedirs(base_dir + class_id)
                  
                  shutil.copy(file, config.SAVE_PATH + class_id)


# function to keep count of the transfered audio files in the new directories defined by the unique classes                  
def dataset_status():
      for root, dir, files in os.walk('dataset'):
            print(f'There are {len(dir)} folders, and {len(files)} files in {root}')



# function to preprocess and extract fratures from audio files
def extract_features(path):

      # load audio data and sample rate
      audio_data, sample_rate = librosa.load(path,res_type='kaiser_fast')
      
      # extract MFCC Features from audio data with its Sample rate wih a frature dimesion of 40 
      mfcc = librosa.feature.mfcc(y=audio_data,
                              sr=sample_rate,
                              n_mfcc=config.N_DIMS)
      
      # scale the extracted features and transpose to a single dimension vector 
      feature = np.mean(mfcc.T, axis=0)

      return np.array(feature)

def convert_mp3_to_wave(input_file,output_file):
      sound = AudioSegment.from_mp3(input_file)
      sound.export(output_file, format="wav")

def predict(data_path):

      labels = ['an air_conditioner','a car_horn','children_playing','a dog_bark',
          'a drilling_machine','an engine_idling','a gun_shot','a jackhammer sound','a siren',
          'street_music']
      
      model = load_model(config.TRAINED_MODEL_PATH)
      output = extract_features(data_path).reshape(1,-1)
      
      # print(output)
      res = model.predict(output)
      prediction = res.argmax(axis=1)
      return labels[prediction[0]]



if __name__ == '__main__':
      # arrange_files()
      # dataset_status()

      # test_path = 'dataset/dog_bark/344-3-0-0.wav'
      # print(extract_features(test_path))
      # print(predict(config.PREDICTION_PATH))
      pass

