import os, argparse, subprocess
from multiprocessing import Pool

parser = argparse.ArgumentParser(description='Split audio files according to the labels.')

parser.add_argument('--label_folder', type=str, 
					help='Folder containing the label files', required=True)
parser.add_argument('--audio_folder', type=str,
                    help='Folder containing the audio files to be split', required=True)
parser.add_argument('--out_folder', type=str,
                    help='Path to store the split audio files', required=True)

args = parser.parse_args()

label_files = os.listdir(args.label_folder)

def splitAudio(file):

    if 'label.txt' not in file:
        print(f"{file} is not a valid labels path")
        return file
    
    file_name = file[:-10] + '.wav'
    label_path = os.path.join(args.label_folder, file)
    audio_path = os.path.join(args.audio_folder, file_name)
    cmd = f"python3 split_audio_files.py --label_file {label_path} \
            --audio_file {audio_path} \
            --out_folder {args.out_folder}"
    print(cmd)
    subprocess.call(cmd, shell=True)

    return file


if __name__ == '__main__':
    pool = Pool()
    a = pool.map(splitAudio, label_files)
    for i in a:
        print(f"\nCompleted processing of file {i}\n")