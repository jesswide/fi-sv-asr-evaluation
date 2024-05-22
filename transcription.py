import sys
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import torchaudio
import os
import json
import re

# Usage: python transcription.py <directory_path>
# <directory_path> should be the path to the directory containing the .wav files.
# Example: python transcription.py /path/to/audio_files

processor = Wav2Vec2Processor.from_pretrained("KBLab/wav2vec2-large-voxrex-swedish")
model = Wav2Vec2ForCTC.from_pretrained("KBLab/wav2vec2-large-voxrex-swedish")

def load_and_preprocess_audio(audio_path):
    waveform, sr = torchaudio.load(audio_path)
    input_values = processor(waveform.squeeze().numpy(), return_tensors="pt", padding="longest", sampling_rate=16000).input_values
    return input_values

def transcribe_audio(input_values):
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)
    return transcription[0]

def process_directory(directory_path):
    results = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".wav"):  # Assuming audio files are in WAV format
            audio_path = os.path.join(directory_path, filename)
            input_values = load_and_preprocess_audio(audio_path)
            hypothesis = transcribe_audio(input_values)
            correct_transcript_path = os.path.join(directory_path, os.path.splitext(filename)[0] + '.trn')
            with open(correct_transcript_path, 'r') as f:
                reference = f.read()
            filename_list = re.split(r"[-.]", filename)
            results.append({
                 'filename' : filename.split(".")[0],
                 'mpid': filename_list[0],
                 'session_number': filename_list[1],
                 'session_year': filename_list[2],
                 'startsec': filename_list[3],
                 'endsec': filename_list[4],
                 'hypothesis': hypothesis,
                 'reference': reference
            })
    return results        

def process_all_directories(main_directory_path):
    all_results = []
    for root, dirs, files in os.walk(main_directory_path):
        for dir in dirs:
            directory_path = os.path.join(root, dir)
            all_results.extend(process_directory(directory_path))
    with open('fi-sv-parliment-transcripts.json', 'w') as json_file:
         json.dump(all_results, json_file, ensure_ascii=False, indent=4)

def main(argv):
    main_directory_path = argv
    process_all_directories(main_directory_path)
    
if __name__ == "__main__":
    main(sys.argv)  