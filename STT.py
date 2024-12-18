import sounddevice as sd
import whisper
import keyboard
import pyautogui
import numpy as np

class SpeechToText:
    def __init__(self, stt_model, hotkey="ctrl+shift+r", sample_rate=16000, idle_timeout=5):
        self.stt_model = stt_model
        self.hotkey = hotkey
        self.sample_rate = sample_rate
        self.recording = False
        self.audio_buffer = []

    def toggle_recording(self):
        """Wechselt zwischen Starten und Stoppen der Aufnahme."""
        if not self.recording:
            self.start_recording()
        else:
            self.transcribe_and_write()

    def start_recording(self):
        """Startet die Audioaufnahme und speichert die Daten im Puffer."""
        print("Aufnahme gestartet...")
        
        self.audio_buffer = []      # clear buffer before starting a recording
        self.recording = True       # set flag for active recording

        # define callback function
        def callback(indata, frames, time, status):
            if self.recording:
                self.audio_buffer.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=self.sample_rate, channels=1, dtype='float32', callback=callback
        )
        self.stream.start()

    def stop_recording(self):
        """Stoppt die Audioaufnahme und gibt die gesammelten Daten zurück."""
        print("Aufnahme beendet.")
        self.recording = False
        self.stream.stop()
        self.stream.close()
        audio = np.concatenate(self.audio_buffer, axis=0).flatten()
        self.audio_buffer = []
        return audio

    def transcribe_and_write(self):
        """Transkribiert die aufgenommene Sprache und schreibt den Text."""
        audio = self.stop_recording()
        text = self.stt_model.transcribe(audio)
        if text:
            pyautogui.write(text)
        else:
            print("Keine Transkription erkannt.")

    def run(self):
        """Startet das Tool und bindet die Hotkeys."""
        keyboard.add_hotkey(self.hotkey, self.toggle_recording)  # Aufnahme starten/stoppen
        print(f"Hotkey {self.hotkey} ist aktiv. Halten Sie die Taste gedrückt, um aufzunehmen.")
        print("Drücken Sie ESC, um das Programm zu beenden.")
        keyboard.wait("esc")


class WhisperModel():
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size, device="cuda")

    def transcribe(self, audio):
        print("Transkribieren mit Whisper...")
        result = self.model.transcribe(audio)
        return result.get('text', '')
    

if __name__ == "__main__":
    Whisper = WhisperModel()
    SpeechToText = SpeechToText(stt_model=Whisper)
    SpeechToText.run()