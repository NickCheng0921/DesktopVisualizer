# DesktopVisualizer

Desktop Audio Visualizer + Transcriber written w/ Tkinter + Pyaudio

![Demo Gif](demos/demo2.2.gif)

Audio is from https://www.youtube.com/watch?v=laXcJyx9xCc

## How to use

Run visualizer.py directly for eq + transcription (requires ffmpeg to be installed on system and in ENV path)

### Notable features

Uses separate threads for pyaudio visual eq and transcription
  - system audio read is blocking and results in window freeze if not threaded separately from tkinter main loop

Relatively lightweight, can run as a background process without overloading system on a legion Y545

### Future work

**EQ**

A-weight or ITU-R 468 reweight audio

Add saturation effect (minor screen flash)

**Transcription**

Fast Diarization + More accurate Transcription

Quantize a larger Whisper model

**Code Clarity**

Combine transcription and eq into one class

### Credits

Transcription framework comes from https://github.com/SevaSk/ecoute, and transcription model is OpenAI's tiny Whisper model.
