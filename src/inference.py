
def process(input_dir, output_dir, model_dir, model, output_format, copy_tags, save_mid, save_lyric):

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
        print(f'❌ Error: Directory {input_dir} does not exist')
        exit()

    for ext in constants.AUDIO_EXTENSIONS:
        audio_files.extend(glob.glob(f'{input_dir}/{ext}'))

    for audio_file in audio_files:

        try:
            audio_file_path = Path(audio_file)
            audio_file_name = audio_file_path.stem
            count += 1

            message = f"Processing {count}/{len(audio_files)}: {audio_file_name}"
            print(message)
            # Separete audio files
            result = separator.separate(audio_file, audio_file_name, model, output_format, output_dir, model_dir)
            instrumental, vocals = result["instrumental"], result["vocals"]

            # Copy original tags
            if copy_tags:
                message = f"Coping Tags {count}/{len(audio_files)}: {audio_file_name}"
                print(message)
                tags.copy_tags(audio_file, audio_file_path, instrumental, vocals, output_format)

            # Convert vocal to MIDI
            if save_mid:
                message = f"Creating midi file {count}/{len(audio_files)}: {audio_file_name}"
                print(message)
                midi.convert_to_midi(vocals, output_dir, audio_file_name)

            # Generate lyrics
            if save_lyric:
                message = f"Generating lyrics {count}/{len(audio_files)}: {audio_file_name}"
                print(message)
                clean_name = clean_filename(vocals.name)
                safe_audio_file = vocals.parent / clean_name

                if vocals != safe_audio_file:
                    shutil.copy(vocals, safe_audio_file)

                # output_path
                output_path = f'{output_dir}/{audio_file_name}'
                
                lyrics.generate_lyrics(str(safe_audio_file), output_path)
                #delete the original file
                if safe_audio_file.exists():
                    safe_audio_file.unlink()

        except Exception as e:
            return print(f"❌ ERROR : {e}")

    print("✅ Process completed!")
