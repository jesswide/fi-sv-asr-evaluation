# ASR Transcription Script

This repository contains a Python script for automatic speech recognition using the Wav2Vec2 2.0 large Swedish model.

The scripts was used as a part of a bachelor thesis in Computer Science.

## Dependencies

- Python 3.x
- Libraries: `transformers`, `torch`, `torchaudio`, `jiwer`, `numpy`

## Installation

No installation is needed for the scripts themselves, simply clone the repository or download the scripts.

Ensure that Python 3 and all dependent libraries are installed. Use the following command to install libraries if not already installed:

```
pip install torch torchaudio transformers numpy jiwer
```

## Executing program

Run each script individually depending on the task. For example:

```
python transcription.py <directory_path>
python wer_calculation.py <directory_path>
python duration.py <directory_path>
python electoral_districts_mapping.py <directory_path> <directory_path>
python metrics.py <directory_path>
python dels_ins_subs_words.py <directory_path>
```

## Authors

[Amanda Gisslen](https://github.com/AmandasRep)

[Jessica Machutta Widengren](https://github.com/jesswide)



