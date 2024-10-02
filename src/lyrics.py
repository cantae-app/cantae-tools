
def generate_lyrics(audio_file):
    import os
    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
    from faster_whisper import WhisperModel

    print("► Generating lyrics")
    model_size = "large-v3"
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    segments, info = model.transcribe(audio_file, beam_size=5, word_timestamps=True, vad_filter=True)

    lyrics = []
    base_filename = audio_file.rsplit('.mp3', 1)[0]
    json_file = base_filename + '.json'
    lrc_file = base_filename + '.lrc'
    line_id = 0
    
    print(json_file, lrc_file)

    with open(lrc_file, 'w', encoding='utf-8') as f_lines:
        for segment in segments:
            start_time = format_time(segment.start)
            text = segment.text
            f_lines.write(f"{start_time}{text}\n")
            if hasattr(segment, 'words'):
                for word in segment.words:
                    lyrics.append({
                        "line_id": line_id,
                        "start": word.start,
                        "end": word.end,
                        "text": word.word,
                    })
            line_id += 1

    import json
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(lyrics, f, ensure_ascii=False, indent=4)

def format_time(time):
    minutes = int(time // 60)
    seconds = int(time % 60)
    milliseconds = int((time % 1) * 100)
    return f"[{minutes:02}:{seconds:02}.{milliseconds:02}]"