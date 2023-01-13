import logging
import boto3
from botocore.exceptions import ClientError
import os, argparse, sys, subprocess
from multiprocessing import Pool

parser = argparse.ArgumentParser(description='STEP1.1 : Upload files to S3 bucket')

parser.add_argument('--wav_folder', type=str, 
					help='Folder containing the audio files', required=True)
parser.add_argument('--aws_folder_path', type=str, 
                    help='S3 bucket to upload the files', required=True)

args = parser.parse_args()

wav_files = os.listdir(args.wav_folder)

def upload_file(file):

    file_name = os.path.join(args.wav_folder, file)
    
    cmd = f"aws s3 cp {file_name} {args.aws_folder_path}"
    subprocess.call(cmd, shell=True)
    print(f"Successfully moved {file} to s3 {args.aws_folder_path}")

    return file


if __name__ == '__main__':
    pool = Pool()
    a = pool.map(upload_file, wav_files)
    for i in a:
        print(f"\nCompleted processing of file {i}\n")