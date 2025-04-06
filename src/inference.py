
def process(input_dir, output_dir, model, output_format, copy_tags, save_mid, save_lyric):

    from pathlib import Path
    import src.midi as midi
    import src.tags as tags
    import glob
    import src.separator as separator
    import src.constants as constants
    import src.lyrics as lyrics
    import unicodedata
    import shutil

    def clean_filename(filename):
        nfkd = unicodedata.normalize('NFKD', filename)
        only_ascii = nfkd.encode('ASCII', 'ignore').decode('ASCII')
        clean_name = only_ascii.replace(' ', '_').replace('&', 'and')
        return clean_name

    audio_files = []
    count = 0

    #check if the directory exists
    if not Path(input_dir).exists():
        print(f'Error: Directory {input_dir} does not exist')
        exit()

    for ext in constants.AUDIO_EXTENSIONS:
        audio_files.extend(glob.glob(f'{input_dir}/{ext}'))

    for audio_file in audio_files:

        try:
            audio_file_path = Path(audio_file)
            audio_file_name = audio_file_path.stem
            count += 1

            print(f"► Starting {count}/{len(audio_files)}: ", audio_file_name)

            # Separete audio files
            primary_stem_file, secondary_stem_file = separator.separate(audio_file, audio_file_name, model, output_format, output_dir)

            # Copy original tags
            if copy_tags:
                tags.copy_tags(audio_file, audio_file_path, primary_stem_file, secondary_stem_file, output_format)

            # Convert vocal to MIDI
            if save_mid:
                midi.convert_to_midi(secondary_stem_file, output_dir, audio_file_name)

            # Generate lyrics
            if save_lyric:
                secondary_stem_path = Path(secondary_stem_file)
                clean_name = clean_filename(secondary_stem_path.name)
                safe_audio_file = secondary_stem_path.parent / clean_name

                if secondary_stem_path != safe_audio_file:
                    shutil.copy(secondary_stem_file, safe_audio_file)

                lyrics.generate_lyrics(str(safe_audio_file))

        except Exception as e:
            return print(f"ERROR : {e}")

    print("► Process completed!")
