import os, argparse, subprocess
import boto3
from multiprocessing import Pool

parser = argparse.ArgumentParser(description='STEP2 : Create and Download Transcripts')

parser.add_argument('--bucket', type=str, 
					help='S3 bucket where the audio files are stored', required=True)
parser.add_argument('--s3_folder', type=str, 
					help='S3 folder containing the wav files', required=True)
parser.add_argument('--out_folder', type=str, 
					help='[Local] output folder path to store the Transcription files (JSON)', required=True)
parser.add_argument('--lang_code', default='hi-IN', type=str, 
		            help='AWS Transcribe language code to generate the transcripts (hi-IN) for hindi')
parser.add_argument('--media_format', default='wav', type=str, 
		            help='Media format of the audio files')
parser.add_argument('--region', default='us-east-1', type=str, 
					help='AWS Region to create the transcription jobs')


args = parser.parse_args()
s3 = boto3.resource('s3')

my_bucket = s3.Bucket(args.bucket)
audio_files = []

for object_summary in my_bucket.objects.filter(Prefix=args.s3_folder):
    if(object_summary.key[-4:] == '.wav'):
        audio_files.append(object_summary.key)
    # print(object_summary.key)

def downTranscripts(file):

    cmd = f"python3 download_transcripts.py --bucket {args.bucket} \
            --out_folder {args.out_folder} \
            --file_name {file} \
            --lang_code {args.lang_code} \
            --media_format {args.media_format} \
            --region {args.region}"
    print(cmd)
    subprocess.call(cmd, shell=True)

    return file


if __name__ == '__main__':
    pool = Pool()
    a = pool.map(downTranscripts, audio_files)
    for i in a:
        print(f"\nCompleted processing of file {i}\n")