"""
Input .txt file containing labels to create smaller audio chunks
"""
import os, argparse
from pydub import AudioSegment

parser = argparse.ArgumentParser(description='Split audio files according to the labels.')

parser.add_argument('--label_file', type=str, 
					help='Label file to split the audio file into chunks', required=True)
parser.add_argument('--audio_file', type=str,
                    help='Path to the audio file to be split', required=True)
parser.add_argument('--out_folder', type=str,
                    help='Path to store the split audio files', required=True)

args = parser.parse_args()


file_path = args.label_file
print(f"Getting labels from file {file_path}")
f = open(file_path, 'r')

audio_path = args.audio_file
print(f"Loading file {audio_path}")
audio = AudioSegment.from_wav(audio_path)

for labels in f:
    labels = labels.strip('\n')
    l = labels.split('\t')
    tmin = float(l[0]) * 1000
    tmax = float(l[1]) * 1000
    file_name = l[2] + '.wav'
    out_file = os.path.join(args.out_folder, file_name) 
    newAudio = audio[tmin: tmax]
    newAudio.export(out_file, format='wav')
    print(f"Exported file {out_file} successfully")

