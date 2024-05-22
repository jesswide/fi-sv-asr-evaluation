import json
import statistics
import sys
import numpy as np

# Usage: python dels_ins_subs_words.py <directory_path>
# <directory_path> should be the path to the directory containing JSON file created by wer_calculation.py
# Example: python transcription.py /path/to/JSON file

def get_transcripts(json_file_path):
    with open(json_file_path, 'r') as json_file:
        transcripts = json.load(json_file)

    return transcripts

def mean_wer_score(transcripts):
    wer_scores = [transcript['wer_score'] for transcript in transcripts]
    return statistics.mean(wer_scores) * 100

def std_dev_all_transcripts(transcripts):
        wer_scores = [transcript['wer_score'] for transcript in transcripts]
        return np.std(wer_scores)

    
def sorted_by_score(transcripts, field, fromHightoLow):
    sorted_transcripts = sorted(transcripts, key=lambda x: x[field], reverse=fromHightoLow)

    for transcript in sorted_transcripts:
        transcript[field] *= 100

    return sorted_transcripts

def highest_wer_by_mpid(transcripts):
    mpid_scores = {}
    for transcript in transcripts:
        mpid = transcript['mpid']
        wer_score = transcript['wer_score'] * 100  
        district = transcript['electoral_district']  

        if mpid not in mpid_scores:
            mpid_scores[mpid] = {'total_score': wer_score, 'count': 1, 'district': district}
        else:
            mpid_scores[mpid]['total_score'] += wer_score
            mpid_scores[mpid]['count'] += 1

    for mpid in mpid_scores:
        mpid_scores[mpid]['mean_score'] = mpid_scores[mpid]['total_score'] / mpid_scores[mpid]['count']

    sorted_mpid_scores = sorted(mpid_scores.items(), key=lambda x: x[1]['mean_score'], reverse=True)

    return sorted_mpid_scores

def highest_wer_by_district(transcripts):
    district_scores = {}
    for transcript in transcripts:
        district = transcript['electoral_district']  
        wer_score = transcript['wer_score'] * 100

        if district in district_scores:
            district_scores[district]['total_score'] += wer_score
            district_scores[district]['count'] += 1
        else:
            district_scores[district] = {'total_score': wer_score, 'count': 1}

    for district in district_scores:
        district_scores[district]['mean_score'] = district_scores[district]['total_score'] / district_scores[district]['count']
    
    sorted_district_scores = sorted(district_scores.items(), key=lambda x: x[1]['mean_score'], reverse=True)

    return sorted_district_scores

def std_dev_by_district(transcripts):
    district_scores = {}

    for transcript in transcripts:
        district = transcript['electoral_district']  
        wer_score = transcript['wer_score'] * 100

        if district in district_scores:
            district_scores[district].append(wer_score)
        else:
            district_scores[district] = [wer_score]

    districts_std_dev = []
    for district, scores in district_scores.items():
        sd = np.std(scores)
        districts_std_dev.append((district, sd)) 

    return districts_std_dev

def main(argv):
    json_file_path = argv
    transcripts = get_transcripts(json_file_path)
    mean_wer_score(transcripts)
    std_dev_all_transcripts(transcripts)
    sorted_by_score(transcripts, 'wer_score', True)
    highest_wer_by_mpid(transcripts)
    highest_wer_by_district(transcripts)
    sorted_by_score(transcripts, 'wer_score', False)
    std_dev_by_district(transcripts)

if __name__ == "__main__":
    main(sys.argv)