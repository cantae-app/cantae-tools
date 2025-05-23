from audio_separator.separator import Separator
from pathlib import Path
import tempfile

def separate(audio_file, file_name, model_filename, output_format, output_dir, model_dir = tempfile.gettempdir()):

    output_names = {
        "Vocals": f'{file_name} - (Vocals)',
        "Instrumental": f'{file_name} - (Instrumental)',
    }

    separator = Separator(
        output_format=output_format,
        output_dir=output_dir,
        model_file_dir=model_dir,
    )

    separator.load_model(model_filename=model_filename)
    primary_stem_path, secondary_stem_path = separator.separate(audio_file,output_names)

    # check primary_stem_path and secondary_stem_path is instrumental and vocals respectively
    if 'Vocals' in primary_stem_path:
        primary_stem_path, secondary_stem_path = secondary_stem_path, primary_stem_path

    instrumental_path = Path(f'{output_dir}/{primary_stem_path}')
    vocals_path = Path(f'{output_dir}/{secondary_stem_path}')

    print(f"✅ Finished Instrumental Path {instrumental_path}")
    print(f"✅ Finished Vocals Path {vocals_path}")

    return {
        "instrumental": instrumental_path,
        "vocals": vocals_path
    }