import speech_recognition as sr
import pyttsx3
import pyaudio
# from fuzzywuzzy.fuzz import ratio
from selenium import webdriver
import random
import os

micro = sr.Microphone()
recognize = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def talk(word):
    engine.say(word)
    engine.runAndWait()


def listen():
    text = ''
    print('Good day. I am listening to you, you can start talking')
    while text == '':
        with micro as sourse:
            recognize.adjust_for_ambient_noise(sourse)
            audio = recognize.listen(sourse, phrase_time_limit=4)
            try:
                text = (recognize.recognize_google(audio, language="ru-Ru")).lower()
                print(f'You said  "{text}"')
            except(sr.UnknownValueError):
                print('I did not understand you or you did not say anything, please try again.')
            except(TypeError):
                pass
        return text


def command(text):
    def open_browser():
        driver = webdriver.Chrome()
        driver.get('https://www.google.com/')

    def hi():
        talk('Hello. Glad to see you. What you want ?')

    def presentation():
        print('Hello. I am a voice bot assistant. I can open your browser, tell you what time it is, turn on fairy'
              ' tales for the kids and much more. Nice to meet you')
        talk('Hello. I am a voice bot assistant. I can open your browser, tell you what time it is, turn on fairy'
             ' tales for the kids and much more. Nice to meet you')

    def bye():
        talk('Goodbye. I was glad to help you')
        exit()

    def fairy_tale():
        driver = webdriver.Chrome()
        driver.get('https://deti-online.com/audioskazki/')
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/label/select/option[4]').click()
        driver.implicitly_wait(10)
        all_tales_raw = driver.find_element_by_id('dt').find_elements_by_tag_name('a')
        all_tales = [href.get_attribute('href') for href in all_tales_raw]
        random_tale = random.choice(all_tales)
        driver.get(random_tale)
        driver.implicitly_wait(10)
        btn_play = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/div[1]/button')
        driver.implicitly_wait(10)
        btn_play.click()

    def swearing():
        talk('You swear. I do not want to answer you anything')
        exit()

    def find_in_internet(cut_text):
        driver = webdriver.Chrome()
        driver.get('https://www.google.com/')
        driver.implicitly_wait(10)
        driver.find_element_by_name('q').send_keys(cut_text + '\n')

    try:
        dict_commands = {
            ('найди', 'загугли', 'найти', 'отыскать', 'отыщи'): find_in_internet,
            ('привет', 'здравствуйте', 'здорово', 'салют', 'добрый день', 'доброе утро', 'добрый вечер'): hi,
            ('представься', 'кто ты', 'что ты такое', 'как тебя зовут', 'как твое имя', 'кто вы',): presentation,
            ('пока', 'прощай', 'покеда', 'удачи', 'всего доброго', 'доброй ночи', 'до свидания', 'сладких снов'): bye,
            ('козел', 'урод', 'тварь', 'крыса'): swearing,
            ('открой браузер',): open_browser,
            ('сказка', 'хочу сказку', 'послушать сказку', 'сказки', 'сказка на ночь', 'хочу сказку',): fairy_tale,
        }
        text.split(' ')
        for cmd in dict_commands:
            if text in cmd:
                dict_commands[cmd]()
            else:
                for i in list(dict_commands.keys())[0]:
                    if i in text:
                        try:
                            excess = list(dict_commands.keys())[0]
                            for word in excess:
                                text = text.replace(word, '')
                            dict_commands[list(dict_commands.keys())[0]](text)
                        except Exception as ex:
                            print(ex)

    except Exception as ex:
        print(ex)


while True:
    command(listen())
