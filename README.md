<p align="center">
    <img src="assets/logo.png" height="50">
</p>

# Cantaê AI Tools

Easily separate vocals and instruments, copy tags, generate MIDI files, and generate lyrics.

<p align="center">
    <img src="assets/preview.png" >
</p>

## Features
- Separate audio into two stems: instrumental and vocals.
- Supports all common audio formats (WAV, MP3, FLAC, M4A, etc.).
- Copy ID3 tags to stems.
- Generate MIDI files from vocals used in the score.
- Generate lyrics.

## Commands
```
# Run dev
flet run main.py -d

# Build app
flet build windows -v

# Packaging desktop app
flet pack src/main.py --name "catae_tools" --icon "src/assets/icon.png" --product-name "Cantaê Tools" --product-version "1.0.0"

```


You may need to reinstall both packages directly, allowing pip to calculate the right versions for your platform, for example:

- `pip uninstall torch onnxruntime`
- `pip cache purge`
- `pip install --force-reinstall torch torchvision torchaudio`
- `pip install --force-reinstall onnxruntime-gpu`

I generally recommend installing the latest version of PyTorch for your environment using the command recommended by the wizard here:
<https://pytorch.org/get-started/locally/>

- `pip install flet==0.27.6`
- `pip install mutagen`
- `pip install faster_whisper`
- `pip install audio-separator[gpu]`
- `pip install basic-pitch[tf]`
