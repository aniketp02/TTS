import logging
import sys, uuid
import time
import boto3
import json
from botocore.exceptions import ClientError
import requests
import os, argparse

from custom_waiter import CustomWaiter, WaitState

parser = argparse.ArgumentParser(description='Create and download the Transcript from AWS Transcribe')

parser.add_argument('--bucket', type=str, 
					help='S3 bucket where the audio files are stored', required=True)
parser.add_argument('--out_folder', type=str, 
					help='[Local] output folder path to store the Transcription files (JSON)', required=True)
parser.add_argument('--file_name', type=str, 
                    help='Name of the file on AWS S3 bucket, The object key and file name shld be same on S3', required=True)
parser.add_argument('--lang_code', default='en-IN', type=str, 
		            help='AWS Transcribe language code to generate the transcripts (hi-IN) for hindi')
parser.add_argument('--media_format', default='wav', type=str, 
		            help='Media format of the audio files')
parser.add_argument('--region', default='us-east-1', type=str, 
					help='AWS Region to create the transcription jobs')


args = parser.parse_args()
logger = logging.getLogger(__name__)

class TranscribeCompleteWaiter(CustomWaiter):
    """
    Waits for the transcription to complete.
    """
    def __init__(self, client):
        super().__init__(
            'TranscribeComplete', 'GetTranscriptionJob',
            'TranscriptionJob.TranscriptionJobStatus',
            {'COMPLETED': WaitState.SUCCESS, 'FAILED': WaitState.FAILURE},
            client)

    def wait(self, job_name):
        self._wait(TranscriptionJobName=job_name)

def start_job(
        job_name, media_uri, media_format, language_code, transcribe_client,
        vocabulary_name=None):
    """
    Starts a transcription job. This function returns as soon as the job is started.
    To get the current status of the job, call get_transcription_job. The job is
    successfully completed when the job status is 'COMPLETED'.

    :param job_name: The name of the transcription job. This must be unique for
                     your AWS account.
    :param media_uri: The URI where the audio file is stored. This is typically
                      in an Amazon S3 bucket.
    :param media_format: The format of the audio file. For example, mp3 or wav.
    :param language_code: The language code of the audio file.
                          For example, en-US or ja-JP
    :param transcribe_client: The Boto3 Transcribe client.
    :param vocabulary_name: The name of a custom vocabulary to use when transcribing
                            the audio file.
    :return: Data about the job.
    """
    try:
        job_args = {
            'TranscriptionJobName': job_name,
            'Media': {'MediaFileUri': media_uri},
            'MediaFormat': media_format,
            'LanguageCode': language_code}
        if vocabulary_name is not None:
            job_args['Settings'] = {'VocabularyName': vocabulary_name}
        response = transcribe_client.start_transcription_job(**job_args)
        job = response['TranscriptionJob']
        logger.info("Started transcription job %s.", job_name)
    except ClientError:
        logger.exception("Couldn't start transcription job %s.", job_name)
        raise
    else:
        return job


def get_job(job_name, transcribe_client):
    """
    Gets details about a transcription job.

    :param job_name: The name of the job to retrieve.
    :param transcribe_client: The Boto3 Transcribe client.
    :return: The retrieved transcription job.
    """
    try:
        response = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name)
        job = response['TranscriptionJob']
        logger.info("Got job %s.", job['TranscriptionJobName'])
    except ClientError:
        logger.exception("Couldn't get job %s.", job_name)
        raise
    else:
        return job


ACCESS_ID = os.getenv('MY_ACCESS_KEY_ID') # AWS credentials
ACCESS_KEY = os.getenv('MY_SECRET_ACCESS_KEY')


s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY)
transcribe_client = boto3.client('transcribe', region_name=args.region, aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY)


media_file_name = args.file_name
media_object_key = args.file_name
transcript_name = args.file_name.split('/')[-1][:-4]
transcript_job = transcript_name + uuid.uuid4().hex
media_uri = f's3://{args.bucket}/{media_object_key}'
print(f"Starting transcription job {transcript_job}.")

start_job(
    transcript_job, f's3://{args.bucket}/{media_object_key}', args.media_format, args.lang_code,
    transcribe_client)
transcribe_waiter = TranscribeCompleteWaiter(transcribe_client)
transcribe_waiter.wait(transcript_job)
job_simple = get_job(transcript_job, transcribe_client)
transcript_simple = requests.get(
    job_simple['Transcript']['TranscriptFileUri']).json()
print(f"Transcript for job {transcript_simple['jobName']}:")
transcript_line = transcript_simple['results']['transcripts'][0]['transcript']
print(transcript_line) #This prints the transcripts of the audio file

# To store the transcripts in a text file;
with open('transcripts_all.txt', 'a+') as f:
    line = args.file_name + '|'+transcript_line
    f.write(line)
    f.write('\n')
    f.write('\n')
f.close()
    

# This code downloads the json transcription files with all other metadata like start time, 
# endtime, confidence etc from aws transcribe
job_simple = get_job(transcript_job, transcribe_client)
transcript_simple = requests.get(job_simple['Transcript']['TranscriptFileUri']).json()


json_file = args.out_folder + transcript_name + '.json' #json file name to store the transcription details

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(transcript_simple, f, ensure_ascii=False, indent=4)
print(f"Downloaded the json file for job {transcript_job}")