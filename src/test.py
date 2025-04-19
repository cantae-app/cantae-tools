import inference as inference

input_directory_path = 'C:/Users/Luciano/Music/Deezer Download/Normais/'
output_directory_path = 'C:/Users/Luciano/Music/Deezer Download/Cantae/'
output_model_path = 'C:/Users/Luciano/Downloads/models'
model = 'UVR_MDXNET_KARA.onnx'
output_format = 'mp3'

inference.process(
  input_directory_path,
  output_directory_path,
  output_model_path,
  model,
  output_format,
  True,
  True,
  False
)