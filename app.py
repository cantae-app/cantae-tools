from pathlib import Path
import midi
import tags
import glob
import separator

directory = 'C:/Users/luciano.oliveira/Music/Normais'
model_filename = 'UVR_MDXNET_KARA_2.onnx'
output_format = 'mp3'
output_dir = 'C:/Users/luciano.oliveira/Music/Separadas'
audio_extensions = ['*.mp3', '*.wav', '*.flac', '*.aac', '*.ogg']
audio_files = []
count = 0

#check if the directory exists
if not Path(directory).exists():
    print(f'Error: Directory {directory} does not exist')
    exit()

for ext in audio_extensions:
    audio_files.extend(glob.glob(f'{directory}/{ext}'))

for audio_file in audio_files:

    audio_file_path = Path(audio_file)
    audio_file_name = audio_file_path.stem
    count += 1


    print(f"► Starting {count}/{len(audio_files)}: ", audio_file_name)

    # Separete audio files
    primary_stem_file, secondary_stem_file = separator.separate(audio_file, audio_file_name, model_filename, output_format, output_dir)

    # Copy original tags
    tags.copy_tags(audio_file, audio_file_path, primary_stem_file, secondary_stem_file, output_format)

    # Convert vocal to MIDI
    midi.convert_to_midi(primary_stem_file, output_dir, audio_file_name)


print("► Process completed!")
