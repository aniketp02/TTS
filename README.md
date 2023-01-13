# TTS
Code for TTS data transcription and data cleaning for audio datasets.

# Pipelines
## Pipeline1

You have the raw audio file chunks and need to split it into smaller audio clips (~10 secs)

- `step1_convert_audio_files.py` convert's the audio files from stereo to mono and to the mentioned framerate.
- `step1.1_upload_to_s3.py` upload the converted files obtained from step1 to S3 bucket
- `step2_transcripts.py` generates and downloads the transcripts from AWS Transcribe (**provide the correct language code**)
- `step3_json_to_labels.py` generates the labels for splitting the larger audio chunks into smaller clips and their corresponding metadata(transcripts)
- `step4_split_audio.py` splits the audio files into smaller clips(~10secs)

## Pipeline2

You have the split audio clips (~10secs) and need to generate the transcript for them
- `step1_convert_audio_files.py` convert's the audio files from stereo to mono and to the mentioned framerate.
- `step1.1_upload_to_s3.py` upload the converted files obtained from step1 to S3 bucket
- `step2_transcripts.py` generates and downloads the transcripts from AWS Transcribe (**provide the correct language code**)
- `step2.2_json_to_metadata.py` generates the metadata(transcripts) for the downloaded json files
