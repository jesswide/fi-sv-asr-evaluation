import json
import sys

# Usage: python duration.py <directory_path>
# <directory_path> should be the path to the directory containing JSON file created by transcripts.py
# Example: python transcription.py /path/to/JSON file

def calculate_duration(transcripts):
    for transcript in transcripts:
        start_sec = int(transcript['startsec'])  
        end_sec = int(transcript['endsec']) 
        duration = (end_sec - start_sec) / 100.0 

        # Eller skriva ut det bara?
        transcript['duration (sec)'] = duration 

        # Save the updated transcripts to a new JSON file
        with open('fi-sv-parliment-transcripts.json', 'w') as json_file:
            json.dump(transcripts, json_file, ensure_ascii=False, indent=4)

def main(argv):
    json_file_path = argv
    with open(json_file_path, 'r') as json_file:
        transcripts = json.load(json_file)
    calculate_duration(transcripts)

if __name__ == "__main__":
    main(sys.argv)