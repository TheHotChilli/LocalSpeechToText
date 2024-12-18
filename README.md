
# Speech-to-Text Tool

A python based easy-to-use Speech-to-Text tool that runs locally on your Windows. 
It uses [OpenAI's Whisper library](https://github.com/openai/whisper) to transcribe speech into text. 
The tool can be activated and deactivated via a custom hotkey, allowing you to dictate text directly into applications such as ChatGPT, Word, or any other software that accepts keyboard input.


## Setup & installation

I used Python 3.11 but the code is expected to be compatible with Python 3.8-3.11. 
The tool depends on a few python packages, mainly [OpenAI's Whisper](https://github.com/openai/whisper), sounddevice, keyboard and pyautogui. 
You need to install the dependencies running
```bash
   pip install sounddevice whisper pyautogui keyboard
```
or using the `requirements.txt` file:
```bash
   pip install -r requirements.txt
```

**GPU Support (Optional):**

If you have a nvidia graphics card and wan't to leverage GPU acceleration for faster transcription, you need to manually install PyTorch with CUDA support, 
as `whisper` installs `torch` with CPU-only support by default. Follow the instructions on the [official PyTorch website]((https://pytorch.org/get-started/locally/)) to install the correct torch version for your system. 
Afterwards the tool will utilize GPU acceleration automatically. 

## Usage

1. Ensure all dependencies are installed.
2. Run the tool using the following command:

   ```bash
   python speech_to_text_tool.py
   ```

3. The tool will now wait for hotkey input. Press the defined hotkey combination `ctrl+shift+r` to start the recording.
4. Press the same hotkey again to stop the recording. The transcribed text will be inserted into the active application. (Note: transcribing might take some time)

<!-- ## Customizing Hotkeys

You can customize the hotkey combination used to start and stop the recording by modifying the `STT.py` file. -->

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
