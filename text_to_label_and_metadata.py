""" 
Takes in input the .txt file generated by running json_to_text.py and outputs 2 files 
One containing all the labels to split the audio files in smaller chunks(split_audio_files.py)
and the other containing the metadata in the required format for training purposes
"""
import os, argparse
import sys
import numpy as np

data = None

parser = argparse.ArgumentParser(description='Generate a txt file containing words and punctuations in the transcript \
                                                along with their start and end times')

parser.add_argument('--input_path', type=str, 
					help='Text file to generate metadata and labels', required=True)
parser.add_argument('--wav_folder', type=str, default='temp/',
                    help='path to the wav folder (can be empty)')

args = parser.parse_args()


text_path = args.input_path
track_id = args.input_path.split('/')[-1][:-4]

if 'txt' not in text_path:
    print("Please provide valid text file path")
    sys.exit(1)

label_path = text_path[:-4]+'_label.txt'
metadata_path = text_path[:-4]+'_metadata.txt'

with open(text_path, 'r') as f:
    data = f.read()
    data = data.split('\n')[:-1]
    
track_name = '{}_'.format(track_id)
k = 0 
final_lab = ""
metadata = ""
st, et = -1,-1
words = []
t_min = 6 # Min duration of audio chunk
t_max = 12 # Max duration of audio chunk
x = np.random.randint(t_min,t_max) 

for line in data:
    dur = et-st
    if dur>x:
        sent = " ".join(words)
        track_upd = track_name + str(k)
        k += 1
        l1 = "{}\t{}\t{}\n".format(st,et,track_upd)
        file_path = os.path.join(args.wav_folder, track_upd)
        l2 = "{}.wav|{}\n".format(file_path, sent)
        x = np.random.randint(t_min,t_max)
        #print(l1, l2)
        final_lab += l1
        metadata += l2
        st = -1
        et = -1
        words = []
    word, stime, etime = line.split('\t')
    stime = float(stime)
    etime = float(etime)
    if st == -1:
        st = stime
    et = etime
    if etime-stime==0:
        if len(words):
            words[-1] = words[-1]+word
    else:
        words.append(word)
    

if len(words) and (et-st)>1:
    sent = " ".join(words)
    track_upd = track_name + str(k)
    k += 1
    l1 = "{}\t{}\t{}\n".format(st,et,track_upd)
    file_path = os.path.join(args.wav_folder, track_upd)
    l2 = "{}.wav|{}\n".format(file_path, sent)
    x = np.random.randint(t_min,t_max)
    final_lab += l1
    metadata += l2
    
with open(metadata_path, 'w') as f:
    f.write(metadata)
print("Successfully saved metadata file at:",metadata_path)

with open(label_path, 'w') as f:
    f.write(final_lab)
print("Successfully saved label file at:",label_path)