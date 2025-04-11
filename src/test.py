import separator

audio_file = 'C:/Users/Luciano/Music/Deezer Download/Normais/Clayton & Romário - Morena.mp3'
audio_file_name = 'Clayton & Romário - Morena'
output_format = 'mp3'
output_dir = 'C:/Users/Luciano/Music/Deezer Download/Cantae'
model = 'UVR_MDXNET_KARA.onnx'

primary_stem_file, secondary_stem_file = separator.separate(audio_file, audio_file_name, model, output_format, output_dir)

print(f"Primary stem file: {primary_stem_file}")
print(f"Secondary stem file: {secondary_stem_file}")