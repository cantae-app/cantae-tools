
from mutagen.id3 import ID3
from audio_separator.separator import Separator

def copy_tags(original, file_path, primary, secondary, output_format):

    if(file_path.suffix == '.mp3' and output_format == 'mp3'):
        # try copying tags
        try:
            input_tags = ID3(original)
            primary_tags = ID3(primary)
            secondary_tags = ID3(secondary)
            for tag in input_tags:
                primary_tags[tag] = input_tags[tag]

            for tag in input_tags:
                secondary_tags[tag] = input_tags[tag]

            print("INFO: Copying ID3 tags...")
            primary_tags.save()
            secondary_tags.save()
        except Exception as e:
            print(f"ERROR : {e}")