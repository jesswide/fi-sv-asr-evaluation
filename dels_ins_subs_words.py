import json
import difflib
from collections import Counter
import sys

# Usage: python dels_ins_subs_words.py <directory_path>
# <directory_path> should be the path to the directory containing JSON file created by wer_calculation.py
# Example: python transcription.py /path/to/JSON file

#Ny med alla i ett
def word_metrics(transcripts):
        reference_counter = Counter()
        hypothesis_counter = Counter()
        deletions_counter = Counter()
        instertions_counter = Counter()
        substitutions_counter = Counter()

        for transcript in transcripts:
            reference_text = transcript['reference']
            hypothesis_text = transcript['hypothesis']
            reference_words = reference_text.split()
            hypothesis_words = hypothesis_text.split()
        
            reference_counter.update(reference_words)
            hypothesis_counter.update(hypothesis_words)

            diff = difflib.ndiff(reference_words, hypothesis_words)

            for i, word in enumerate(diff):
                if word.startswith('- '):  # Indicates a deletion in difflib's output
                    deletions_counter[word[2:]] += 1
                    # Check if the next word is an addition, indicating a substitution
                    if i + 1 < len(diff) and diff[i + 1].startswith('+ '):
                        ref_word = word[2:]
                        hyp_word = diff[i + 1][2:]
                        substitutions_counter[(ref_word, hyp_word)] += 1
                if word.startswith('+ '):  # Indicates a deletion in difflib's output
                    instertions_counter[word[2:]] += 1

        deleted_words = deletions_counter.most_common()
        inserted_words = instertions_counter.most_common()
        substituted_words = substitutions_counter.most_common()

        print(deleted_words + inserted_words + substituted_words)

def main(json_file_path):
    with open(json_file_path, 'r') as json_file:
        transcripts = json.load(json_file)
    word_metrics(transcripts)

if __name__ == "__main__":
    json_file_path = sys.argv
    main(json_file_path)
