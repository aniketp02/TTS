import os, argparse
import json, sys

parser = argparse.ArgumentParser(description='STEP2.2 : Generate metadata from json files')

parser.add_argument('--json_folder', type=str, 
					help='Folder containing the audio files', required=True)
parser.add_argument('--wav_folder', type=str, default='temp/',
                    help='path to the wav folder (can be empty)')

args = parser.parse_args()

txt_files = os.listdir(args.json_folder)

def genText(file_path):
    json_path = os.path.join(args.json_folder, file_path)
    metadata_path = json_path[:-4]+'_metadata.txt'

    if 'json' not in json_path:
        print("Please provide valid text file path")
        return json_path
    
    with open(json_path, 'r') as f:
        json_obj = json.load(f)
    
    words = json_obj["results"]['transcripts'][0]['transcript']

    wav_path = os.path.join(args.wav_folder, file_path[:-5])

    metadata = "{}.wav|{}\n".format(wav_path, words)
    print(metadata)

    with open(metadata_path, 'w') as f:
        f.write(metadata)
    print("Successfully saved metadata file at:",metadata_path)
    return json_path


if __name__ == '__main__':
    for file in txt_files:
        genText(file)
        print(f"\nCompleted processing of file {file}\n")