import sounddevice as sd
import whisper
import keyboard         # key based callbacks
import pyautogui        # control of mouse and keyboard
import numpy as np
import threading
from abc import ABC, abstractmethod

### Models

class STTModel(ABC):
    """ Abstract model base class"""
    @abstractmethod
    def transcribe(self, audio):
        """ Call model to perform speech to text transcription"""
        pass

    @abstractmethod
    def load(self):
        """Load model to memory"""
        pass

    @abstractmethod
    def unload(self):
        """Unload model from memory to free space"""
        pass
    
class WhisperModel(STTModel):
    def __init__(self, model_size="base"):
        self.model_size = model_size
        self.model = None

    def load(self):
        if self.model is None:
            self.model = whisper.load_model(self.model_size)
            print(f"Loaded {self.__class__.__name__}")

    def unload(self):
        if self.model is not None:
            del self.model
            self.model = None
            print(f"Deleted {self.__class__.__name__}")

    def transcribe(self, audio):
        if self.model is None:
            self.load()
        print(f"Transcibing with {self.__class__.__name__}...")
        result = self.model.transcribe(audio)
        return result.get('text', '')

### Speech to text

class SpeechToText:
    def __init__(self, stt_model: STTModel, hotkey="ctrl+shift+r", sample_rate=16000, idle_timeout=120):
        self.stt_model = stt_model
        self.hotkey = hotkey
        self.sample_rate = sample_rate
        self.recording = False                  # flag to indicate if a recording is active
        self.audio_buffer = []
        self.idle_timeout = idle_timeout        # timeout in seconds for unloading/deleting laoded model from memory 
        self.timer = None                       # Timer object for performing model unloading

    def start_timer(self):
        """Start a timer that unloads the stt_model after idle-time"""
        # stop existing timer 
        if self.timer:
            self.timer.cancel()
        # start new timer
        self.timer = threading.Timer(self.idle_timeout, self.stt_model.unload())
        self.timer.start()

    def stop_timer(self):
        """Stop the running timer"""
        if self.timer:
            self.timer.cancel()

    def toggle_recording(self):
        """Switch between start and stop of a recording"""
        if not self.recording:
            self.start_recording()
        else:
            self.transcribe_and_write()

    def start_recording(self):
        """Start a audio recording and store the audio data into the buffer"""
        print("Recording started...")
        
        self.audio_buffer = []      # clear buffer before starting a recording
        self.recording = True       # set flag for active recording

        # define callback function that appends stream data to buffer
        def callback(indata, frames, time, status):
            if self.recording:
                self.audio_buffer.append(indata.copy())

        # define and start audio stream
        self.stream = sd.InputStream(
            samplerate=self.sample_rate, channels=1, dtype='float32', callback=callback
        )
        self.stream.start()

    def stop_recording(self):
        """Stops the audio recording and returns the collected data as numpy array"""
        print("Recording stopped.")
        self.recording = False
        self.stream.stop()
        self.stream.close()
        audio = np.concatenate(self.audio_buffer, axis=0).flatten()
        self.audio_buffer = []
        return audio

    def transcribe_and_write(self):
        """Calls stt_models transcribe method and writes the transcribed text"""
        audio = self.stop_recording()
        text = self.stt_model.transcribe(audio)
        if text:
            pyautogui.write(text)
        else:
            print("No transcript recognized.")

    def run(self):
        """Starts the tool and binds the keyboard hotkey."""
        keyboard.add_hotkey(self.hotkey, self.toggle_recording)
        print(f"Hotkey {self.hotkey} is active. Press the hotkey to start a recording. Press the hotkey again to stop the recording.")
        print("Press ESC to exit the program.")
        keyboard.wait("esc")

### Test

if __name__ == "__main__":
    Whisper = WhisperModel()
    SpeechToTextTool = SpeechToText(stt_model=Whisper)
    SpeechToTextTool.run()