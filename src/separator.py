from audio_separator.separator import Separator
from pathlib import Path

def separate(audio_file, file_name, model_filename, output_format, output_dir):

    separator = Separator(
        output_format=output_format,
        output_dir=output_dir,
        model_file_dir='models',
    )

    separator.load_model(model_filename=model_filename)
    primary_stem_path, secondary_stem_path = separator.separate(audio_file)

    # Rename the output files
    primary_stem_name = f'{output_dir}/{file_name} - (Instrumental).{output_format}'
    primary_stem_file = Path(f'{output_dir}/{primary_stem_path}').rename(primary_stem_name);
    secondary_stem_name = f'{output_dir}/{file_name} - (Vocals).{output_format}'
    secondary_stem_file = Path(f'{output_dir}/{secondary_stem_path}').rename(secondary_stem_name);

    return primary_stem_file, secondary_stem_file