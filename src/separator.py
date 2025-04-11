from audio_separator.separator import Separator
from pathlib import Path

def separate(audio_file, file_name, model_filename, output_format, output_dir):

    output_names = {
        "Vocals": f'{file_name} - (Vocals)',
        "Instrumental": f'{file_name} - (Instrumental)',
    }

    separator = Separator(
        output_format=output_format,
        output_dir=output_dir,
        model_file_dir='models',
    )

    separator.load_model(model_filename=model_filename)
    primary_stem_path, secondary_stem_path = separator.separate(audio_file,output_names)

    instrumental_path = Path(f'{output_dir}/{primary_stem_path}')
    vocals_path = Path(f'{output_dir}/{secondary_stem_path}')

    print(f"Instrumental path: {instrumental_path}")
    print(f"Vocals path: {vocals_path}")

    return instrumental_path, vocals_path