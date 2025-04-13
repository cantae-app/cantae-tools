import os
from pathlib import Path
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH

def convert_to_midi(audio_file, output_directory, output_name=None):
    # Verify the file exists
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"❌ File not found: {audio_file}")

    try:
        predict_and_save(
            audio_path_list=[audio_file],  # audio file path
            output_directory=output_directory,  # output directory
            save_midi=True,  # save midi file
            sonify_midi=False,  # save sonified midi file
            save_model_outputs=False,  # save model outputs
            save_notes=False,  # save notes
            model_or_model_path=ICASSP_2022_MODEL_PATH,
            minimum_note_length=11, # Minimum Note Length
            maximum_frequency=3000.0,  # Maximum Pitch
            # minimum_frequency=0.0,  # Minimum Pitch
            frame_threshold=0.30, # Model Confidence Threshold
            onset_threshold=0.90, # Note Segmentation
            multiple_pitch_bends=False,
        )

        # Rename the midi file
        if output_name:
            midi_file = audio_file.stem
            midi_file = f'{midi_file}_basic_pitch.mid'
            midi_rename = f'{output_directory}/{output_name}.mid'
            midi_file = Path(f'{output_directory}/{midi_file}').rename(midi_rename)

    except Exception as e:
        print(f"❌ ERROR: reading or converting audio file: {e}")
        raise