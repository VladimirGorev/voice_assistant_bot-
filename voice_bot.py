import speech_recognition as sr
import pyttsx3
import pyaudio
import os


micro = sr.Microphone()
recognize = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
# engine.setProperty('rate', 120)


def talk(word):
    engine.say(word)
    engine.runAndWait()


def listen():
    text = ''
    with micro as sourse:
        print('Good day. I am listening to you, you can start talking')
        recognize.adjust_for_ambient_noise(sourse, duration=1)
        audio = recognize.listen(sourse, phrase_time_limit=4)
        try:
            text = (recognize.recognize_google(audio, language="ru-Ru")).lower()
            print('You said', text)
        except(sr.UnknownValueError):
            talk("I did not understand you, please try again.")
        except(TypeError):
            pass
    return text


def command(text):
    if 'привет' in text:
        talk('Начало положено')


command(listen())





