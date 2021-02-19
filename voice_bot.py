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
            print(f'You said  "{text}"')
        except(sr.UnknownValueError):
            print('I did not understand you, please try again.')
            talk("I did not understand you, please try again.")
        except(TypeError):
            pass
    return text


def command(text):
    def hi():
        talk('Hello. What you want ?')

    def bye():
        talk('Good bye')

    def sorry():
        talk('Sorry, we do not know what to tell you about this request')

    try:
        dict_commands = {
            'hello': ('привет', 'здравствуйте', 'здорово', 'салют', 'добрый день'),
            'bye': ('пока', 'прощай', 'покеда', 'удачи', 'всего доброго'),
        }
        dict_act = {
            'hello': hi,
            'bye': bye,
            'empty': sorry,
        }

        for cmd in dict_commands:
            for word in dict_commands[cmd]:
                if text == word:
                    task = cmd
                else:
                    task = 'empty'
        dict_act[task]()
    except Exception as ex:
        print(ex)


while True:
    command(listen())
