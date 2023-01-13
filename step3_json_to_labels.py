import os, argparse, subprocess
from multiprocessing import Pool
import sys

parser = argparse.ArgumentParser(description='STEP3 : Generate metadata and labels from the given json files')

parser.add_argument('--in_folder', type=str, 
					help='Folder containing the json transcripts', required=True)
parser.add_argument('--wav_folder', type=str, default='temp/',
                    help='path to the wav folder (can be empty)')

args = parser.parse_args()

json_files = os.listdir(args.in_folder)

def genMetaLabels(file):

    if 'json' not in file:
        print("Please provide valid json path")
        return file
    
    file_path = os.path.join(args.in_folder, file)

    cmd1 = f"python3 json_to_text.py --input_path {file_path}"
    print(cmd1)
    subprocess.call(cmd1, shell=True)
    print("Generate the Text file from the given json file!!")

    txt_file_path = file_path[:-4]+'txt'

    cmd2 = f"python3 text_to_label_and_metadata.py --input_path {txt_file_path} \
            --wav_folder {args.wav_folder}"
    print(cmd2)
    subprocess.call(cmd2, shell=True)
    print("Successfully generated Metadata and Labels")

    return file


if __name__ == '__main__':
    pool = Pool()
    a = pool.map(genMetaLabels, json_files)
    for i in a:
        print(f"\nCompleted processing of file {i}\n")