from pathlib import Path
import midi
import tags
import glob
import separator
import constants


def process(input_dir, output_dir, model, output_format, separate_audio, copy_tags, save_mid, save_lyric):
    audio_files = []
    count = 0

    #check if the directory exists
    if not Path(input_dir).exists():
        print(f'Error: Directory {input_dir} does not exist')
        exit()

    for ext in constants.AUDIO_EXTENSIONS:
        audio_files.extend(glob.glob(f'{input_dir}/{ext}'))

    for audio_file in audio_files:

        audio_file_path = Path(audio_file)
        audio_file_name = audio_file_path.stem
        count += 1


        print(f"► Starting {count}/{len(audio_files)}: ", audio_file_name)

        # Separete audio files
        if separate_audio:
            primary_stem_file, secondary_stem_file = separator.separate(audio_file, audio_file_name, model, output_format, output_dir)

        # Copy original tags
        if copy_tags:
            tags.copy_tags(audio_file, audio_file_path, primary_stem_file, secondary_stem_file, output_format)

        # Convert vocal to MIDI
        if save_mid:
            midi.convert_to_midi(primary_stem_file, output_dir, audio_file_name)


    print("► Process completed!")
