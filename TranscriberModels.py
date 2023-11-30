#import openai
import whisper
import os
import torch

def get_model(use_api):
    return WhisperTranscriber()

class WhisperTranscriber:
    def __init__(self):
        self.audio_model = whisper.load_model(os.path.join(os.getcwd()+os.sep+'models'+os.sep, 'tiny.en.pt'))
        print(f"[INFO] Whisper using GPU: " + str(torch.cuda.is_available()))

    def get_transcription(self, wav_file_path):
        try:
            result = self.audio_model.transcribe(wav_file_path, fp16=torch.cuda.is_available())
        except Exception as e:
            print(e)
            return ''
        return result['text'].strip()
