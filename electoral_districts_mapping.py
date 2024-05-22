import json
import csv
import sys

# Usage: python transcription.py <transcripts_directory_path> <mapping_directory_path>
# <transcripts_directory_path> should be the path to the directory containing JSON file created by transcripts.py
# <mapping_directory_path> should be the path to the directory containing CSV file with the MPID to electoral district mapping.
# Example: python transcription.py /path/to/json_file /path/to/csv_file 

def load_mpid_district_mapping(csv_file_path):
    mapping = {}
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            mpid, district = row
            mapping[mpid] = district
    return mapping

def update_electoral_district(transcripts, mapping):
    for transcript in transcripts:
        mpid = transcript['mpid'] 
        transcript['electoral_district'] = mapping.get(mpid)

    with open('fi-sv-parliment-transcripts.json', 'w') as json_file:
        json.dump(transcripts, json_file, ensure_ascii=False, indent=4)
    
def main(argv):
    json_file_path = argv[1]
    csv_file_path = argv[2]
    mapping = load_mpid_district_mapping(csv_file_path)
    with open(json_file_path, 'r') as json_file:
        transcripts = json.load(json_file)
    update_electoral_district(transcripts, mapping)

if __name__ == "__main__":
    main(sys.argv)  