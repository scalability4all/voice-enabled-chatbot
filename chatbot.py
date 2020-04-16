import random
import datetime
import webbrowser
import pyttsx3
import wikipedia
from pygame import mixer
import pyowm
import config
import speech_recognition as sr
from google_places import *
import pyjokes
from googletrans import Translator
from voice_conf import *
# from speech_recognition.__main__ import r, audio

greetings = ['hey there', 'hello', 'hi', 'Hai', 'hey!', 'hey', 'hi there!']
question = ['How are you?', 'How are you doing?', 'What\'s up?']
responses = ['Okay', "I'm fine"]
var1 = ['who made you', 'who created you']
var2 = ['I_was_created_by_Edward_right_in_his_computer.',
        'Edward', 'Some_guy_whom_i_never_got_to_know.']
var3 = ['what time is it', 'what is the time', 'time']
var4 = ['who are you', 'what is you name']
var5 = ['date', 'what is the date', 'what date is it', 'tell me the date']
cmd1 = ['open browser', 'open google']
cmd2 = ['play music', 'play songs', 'play a song', 'open music player']
cmd3 = [
    'tell a joke',
    'tell me a joke',
    'say something funny',
    'tell something funny']
cmd4 = ['open youtube', 'i want to watch a video']
cmd5 = ['tell me the weather', 'weather', 'what about the weather', 'what\'s the weather']
cmd6 = ['exit', 'close', 'goodbye', 'nothing', 'catch you later', 'bye']
cmd7 = [
    'what is your color',
    'what is your colour',
    'your color',
    'your color?']
colrep = [
    'Right now its rainbow',
    'Right now its transparent',
    'Right now its non chromatic']
cmd8 = ['what is you favourite colour', 'what is your favourite color']
cmd9 = ['thank you']

repfr9 = ['youre welcome', 'glad i could help you']

personalized, longitude, latitude = get_location()
stores = []
stores_data = {}

print("hi ", "Setting location through ip bias, Change location?")
change_location = False
language_conf = input('Language(en-US): ')
if language_conf == '':
    language_conf = "en-US"
voice_language = getVoiceID(language_conf[:2])

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voice_language)
volume = engine.getProperty('volume')
engine.setProperty('volume', 10.0)
rate = engine.getProperty('rate')

engine.setProperty('rate', rate - 25)

translator = Translator()
while True:
    speech_type = input('Speech/Text: ')
    if speech_type.lower() != "speech":
        translate = input("Type: ")
    else:
        now = datetime.datetime.now()
        r = sr.Recognizer()
        with sr.Microphone() as source:
            t = translator.translate('Say something', dest=language_conf[:2])
            print(t.text)
            engine.say(t.text)
            engine.runAndWait()
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                translate = r.recognize_google(audio, language=language_conf)
                print("You said:- " + translate)
            except sr.UnknownValueError:
                print("Could not understand audio")
                engine.say('I didnt get that. Rerun the code')
                engine.runAndWait()
    translate_split = translate.split(" ")
    if translate in greetings:
        random_greeting = random.choice(greetings)
        print(random_greeting)
    elif translate.lower() == "yes":
        change_location = True
        print("Location?")
    elif change_location is True:
        personalized = change_location_query(translate, config.google_api_key)
        change_location = False
    elif translate in question:
        print('I am fine')
    elif translate in var1:
        reply = random.choice(var2)
        print(reply)
    elif translate in cmd9:
        print(random.choice(repfr9))
    elif translate in cmd7:
        print(random.choice(colrep))
        print('It keeps changing every micro second')
    elif translate in cmd8:
        print(random.choice(colrep))
        print('It keeps changing every micro second')
    elif translate in cmd2:
        mixer.init()
        mixer.music.load("song.wav")
        mixer.music.play()
    elif translate in var4:
        engine.say('I am a bot, silly')
        engine.runAndWait()
    elif translate in cmd4:
        webbrowser.open('http://www.youtube.com')
    elif translate in cmd6:
        print('see you later')
        exit()
    elif translate in cmd5:
        print("here")
        url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units={}".\
              format(latitude, longitude, config.weather_api_key, config.weather_temperature_format)
        r = requests.get(url)
        x = r.json()
        city = x['name']
        windSpeed = x['wind']['speed']
        skyDescription = x['weather'][0]['description']
        maxTemperature = x['main']['temp_max']
        minTemperature = x['main']['temp_min']
        temp = x['main']['temp']
        humidity = x['main']['humidity']
        pressure = x['main']['pressure']
        # use the above variables based on user needs
        print("Weather in {} is {} "
              "with temperature {} celsius"
              ", humidity in the air is {} "
              "and wind blowing at a speed of {}".
              format(city, skyDescription, temp, humidity, windSpeed))

        engine.say("Weather in {} is {} "
                   "with temperature {} celsius"
                   ", humidity in the air is {} "
                   "and wind blowing at a speed of {}".
                   format(city, skyDescription, temp, humidity, windSpeed))
        engine.runAndWait()
    elif translate in var3 or translate in var5:
        current_time = datetime.datetime.now()
        if translate in var3:
            print(current_time.strftime("The time is %H:%M"))
            engine.say(current_time.strftime("The time is %H:%M"))
            engine.runAndWait()
        elif translate in var5:
            print(current_time.strftime("The date is %B %d, %Y"))
            engine.say(current_time.strftime("The date is %B %d %Y"))
            engine.runAndWait()
    elif translate in cmd1:
        webbrowser.open('http://www.google.com')
    elif translate in cmd3:
        jokrep = pyjokes.get_joke()
        print(jokrep)
        engine.say(jokrep)
        engine.runAndWait()
    elif ("them" in translate_split or "popular" in translate_split) and stores:
        sorted_stores_data = sorted(
            stores_data,
            key=lambda x: x['rating'],
            reverse=True)
        sorted_stores = [x['name'] for x in sorted_stores_data][:5]
        if "order" in translate:
            print("These are the stores: ")
            for store in sorted_stores:
                print(store)
            engine.say(sorted_stores)
            engine.runAndWait()
        if "popular" in translate:
            print("Most popular one is: ", sorted_stores[0])
        if "go" in translate:
            lat = sorted_stores_data[0]['geometry']['location']['lat']
            lng = sorted_stores_data[0]['geometry']['location']['lng']
            url = "http://maps.google.com/maps?q={},{}".format(lat, lng)
            webbrowser.open_new(url)
            engine.say(
                "Showing you directions to the store {}".format(
                    sorted_stores[0]))
            engine.runAndWait()
    elif "stores" in translate_split or "food" in translate_split or "restaurant" in translate:
        stores = []
        stores_data = {}
        query = filter_sentence(translate)
        stores, stores_data = nearby_places(
            config.google_api_key, personalized.city, query,
            personalized.latitude, personalized.longitude)
        print("These are the stores: ")
        for store in stores:
            print(store)
        engine.say(stores)
        engine.runAndWait()
        print("Where do you want to go:")
        engine.say("Where do you want to go:")
        engine.runAndWait()
    else:
        engine.say("please wait")
        engine.runAndWait()
        print(wikipedia.summary(translate))
        engine.say(wikipedia.summary(translate))
        engine.runAndWait()
        userInput3 = input("or else search in google")
        webbrowser.open_new('http://www.google.com/search?q=' + userInput3)
