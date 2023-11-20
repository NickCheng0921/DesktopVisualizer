# DesktopVisualizer

Desktop Audio Visualizer App written w/ Tkinter + Pyaudio

![Demo Gif](demo.gif)

## How to use

Run visualizer.py directly, or look in build folder for a windows executable

### Notable features

Uses separate threading for pyaudio system buffer read
  - system audio read is blocking and results in window freeze if not threaded separately from tkinter main loop

### Future work

Faster fft

Balance frequency bin overflow (current frequency display is inaccurate)

A-weight and scale audio for more aesthetic look
