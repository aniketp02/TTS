import os, argparse
import wave
#Also need ffmpeg installed

parser = argparse.ArgumentParser(description='Convert audio files from stereo to mono and change framerate to 22050')

parser.add_argument('--in_folder', type=str, 
					help='Name of folder containing wav files to be preprocessed', required=True)
parser.add_argument('--out_folder', type=str, 
          help='Folder to save the processed wav files', required=True)
parser.add_argument('--frame_rate', default=22050, type=int, 
					help='Frame rate of the wav files')

args = parser.parse_args()

can_scan = False
folder_path = f'{args.in_folder}'

if os.path.isdir(folder_path):
  print(f'Folder name set to {folder_path}.')
  can_scan = True
else:
  print('Invalid folder path.')


if can_scan == True:
  resample_list = []
  for file_name in os.listdir(folder_path):
    if(file_name[-4:] != '.wav'):
      print(f'The provided file: {file_name} is not a .wav file') 
      continue
    with wave.open(folder_path + file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        if frame_rate == args.frame_rate and channels == 1:
          print(f'{file_name} does not require resampling.')
        else:
          print(f'{file_name} requires resampling.')
          resample_list.append(file_name)
else:
  print('Please provide a valid folder path!! The provided file is not a .wav file')

if len(resample_list) > 0:
  need_to_resample = True
  print(f'\nScan completed. Please continue to resample {len(resample_list)} file(s).')
else:
  print('\nThere are no files to resample.')
  need_to_resample = False

if need_to_resample == False:
  print('There is nothing to resample.')
  exit()


for item in resample_list:
  os.system(f'ffmpeg -y -i {folder_path}{item} -ar {args.frame_rate} -ac 1 {args.out_folder}{item}') # Converts to Mono also
  print(f'Resampled file {item}.')