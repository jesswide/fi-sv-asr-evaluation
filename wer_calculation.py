import sys
from jiwer import wer
import json

# Usage: python wer_calculation.py <directory_path>
# <directory_path> should be the path to the directory containing JSON file created by transcripts.py
# Example: python transcription.py /path/to/json_file

def calculate_wer(transcripts):
    for transcript in transcripts:
        reference = transcript['reference']
        hypothesis = transcript['hypothesis']
        wer_score = wer(reference, hypothesis)
        transcript['wer_score'] = wer_score
    with open('fi-sv-parliment-transcripts.json', 'w') as json_file:
        json.dump(transcripts, json_file, ensure_ascii=False, indent=4)

def main(json_file_path):
    with open(json_file_path, 'r') as json_file:
        transcripts = json.load(json_file)
    calculate_wer(transcripts)

if __name__ == "__main__":
    json_file_path = sys.argv 
    main(json_file_path)
