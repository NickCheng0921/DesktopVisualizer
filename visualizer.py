import tkinter as tk
import pyaudiowpatch as pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import os

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
CHUNK = 1024
UPDATE_INTERVAL = 75  # milliseconds

class LiveLogScaleBarChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Sound Frequency Visualizer")

        # PyAudio setup
        self.p = pyaudio.PyAudio()

        try:
            # Get default WASAPI info
            wasapi_info = self.p.get_host_api_info_by_type(pyaudio.paWASAPI)
        except OSError:
            exit()

        # Get default WASAPI speakers
        default_speakers = self.p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])

        if not default_speakers["isLoopbackDevice"]:
            for loopback in self.p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break
            else:
                exit()

        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=default_speakers["maxInputChannels"],
            rate=int(default_speakers["defaultSampleRate"]),
            frames_per_buffer=CHUNK,
            input=True,
            input_device_index=default_speakers["index"]
        )

        # Modify plot look
        self.fig, self.ax = plt.subplots()
        self.fig.set_facecolor('#2E3440')
        self.ax.set_facecolor('#2E3440')
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.xaxis.set_ticks_position('none')
        self.ax.tick_params(axis='x', rotation=45)
        self.fig.subplots_adjust(left=0, right=1, top=1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Initialize data buffer
        self.frequency_bins = [32, 64, 128, 256, 512, 1000, 2000, 4000, 8000, 16000]
        self.ax_ticks = ['32', '64', '128', '256', '512', '1K', '2K', '4K', '8K', '16K']
        self.bar_positions = np.arange(len(self.frequency_bins))

        self.ax.set_xticks(list(range(len(self.frequency_bins))))
        self.ax.set_xticklabels(self.ax_ticks, color='#A3BE8C')

        # Create an initial empty bar chart
        self.bars = self.ax.bar(
            self.bar_positions,
            np.zeros_like(self.frequency_bins),
            color='#A3BE8C',  # Nord Green color

        )
        self.ax.set_ylim(1, 8*1e6)  # Adjust the y-axis limits based on your data
        #plt.axis('off')
        plt.gca().get_yaxis().set_visible(False)
        #plt.tick_params(axis='both', left=False, top=False, right=False, bottom=False, labelleft=False,
        #                labeltop=False, labelright=False, labelbottom=False)

        # Tkinter setup
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Use a thread for audio processing
        self.audio_thread = threading.Thread(target=self.audio_processing_thread)
        self.audio_thread.daemon = True  # The thread will exit when the main program exits
        self.audio_thread.start()

        self.root.after(UPDATE_INTERVAL, self.update)
        self.root.mainloop()

    def audio_processing_thread(self):
        while True:
            # Read audio data
            data = np.frombuffer(self.stream.read(CHUNK, exception_on_overflow=False),
                                  dtype=np.int16)
            # Inside the update method, before computing the FFT
            window = np.hamming(len(data))
            data = data * window
            spectrum = np.fft.fft(data)[:CHUNK // 2]
            amplitude = np.abs(spectrum)

            # Update the shared variable for the main thread to access
            self.amplitude_data = amplitude

    def update(self):
        # Access the shared variable for amplitude data
        amplitude = getattr(self, 'amplitude_data', None)

        if amplitude is not None:
            # Update the bar chart
            for bar, amp in zip(self.bars, amplitude):
                bar.set_height(amp)

            # Draw the updated plot on the Tkinter canvas
            self.canvas.draw()

        # Schedule the next update
        self.root.after(UPDATE_INTERVAL, self.update)

    def on_close(self):
        # Clean up resources when the window is closed
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.root.destroy()
        exit()

if __name__ == "__main__":
    root = tk.Tk()
    icon_path = os.path.abspath('./static/favicon.ico')
    root.iconbitmap(icon_path)
    app = LiveLogScaleBarChartApp(root)
