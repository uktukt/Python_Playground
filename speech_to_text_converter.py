# https://realpython.com/python-speech-recognition/
# https://www.ffmpeg.org/download.html
# pip install SpeechRecognition pydub
# pip install ffmpeg-downloader
# ffdl install --add-path

import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import moviepy.editor as mpy
from moviepy.editor import AudioFileClip, VideoFileClip



select_language = 'en-GB' # English (United Kingdom)
#select_language = 'lt-LT' # Lithuanian

# Import and convert MP3 or MP4 file to a WAV file

input_name = 'audio.mp3'
wav_name = str(input_name[0:-4])+'.wav'
print(wav_name)

def convert_to_wav(input_name, wav_name):
    '''Import and convert MP3 or MP4 file to a WAV file'''
    try:
        if input_name.endswith('.wav'):
            pass
        elif input_name.endswith('.mp3'):
            audio_file = mpy.AudioFileClip(input_name)
            audio_file.write_audiofile(wav_name)
        elif input_name.endswith('.mp4'):
            video = mpy.VideoFileClip(input_name)
            audio = video.audio
            audio.write_audiofile(wav_name)
        else:
            print('wrong file format')
    except Exception as e:
        print(f'An error occurred: {e}')

convert_to_wav(input_name, wav_name)

# Create a speech recognition object
r = sr.Recognizer()

def transcribe_large_audio(wav_name):
    '''Split audio into chunks and apply speech recognition'''
    # Open audio file with pydub
    sound = AudioSegment.from_wav(wav_name)
    # Split audio where silence is > 1500ms
    chunks = split_on_silence(sound, min_silence_len=700, silence_thresh=sound.dBFS-5, keep_silence=100)
    
    # Create folder to store audio chunks
    folder_name = 'audio-chunks'
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    
    whole_text = ''
    # Process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # Export chunk and save in folder
        chunk_filename = os.path.join(folder_name, f'chunk{i}.wav')
        audio_chunk.export(chunk_filename, format='wav')
        # Recognize chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # Convert to text
            try:
                text = r.recognize_google(audio_listened, language=select_language)
                text = f'{i}: {text.capitalize()}. '
            except sr.UnknownValueError as e:
                error_message = f'Error in chunk {i}: {str(e)}. '
                print(error_message)
                text = f'{i}: [Unrecognized]. '
            print(chunk_filename, ':', text)
            whole_text += text + '\n'

    return whole_text

result = transcribe_large_audio(wav_name)
print(result)
print(result, file=open('en.txt', 'w', encoding = 'UTF-8'))
