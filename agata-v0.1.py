from re import search
import speech_recognition as sr
import playsound
from gtts import gTTS, tts
import random
import webbrowser
import pyttsx3
import os


class VirtualAssist():
    def __init__(self, assist_name, person):
        self.person = person
        self.assist_name = assist_name
        
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        
        self.voice_data = ''
        
    def engine_speak(self, text):
        """
        Virtual assistant talk
        """
        text = str(text)
        self.engine.say(text)
        self.engine.runAndWait()
        
    def record_audio(self, ask=""):
        with sr.Microphone() as source:
            if ask:
                print('recording...')
                self.engine_speak(ask)
                
            audio = self.r.listen(source, 5, 5) #Get audio data
            print('Looking at the data base')
            try:
                self.voice_data = self.r.recognize_google(audio) #Convert audio to text
                
            except sr.UnknownValueError:
                self.engine_speak('Sorry Boss, I did not get what you said. Can you please repeat?')
                
            except sr.RequestError:
                self.engine_speak('Sorry Boss, my server is down') # recognizer is not connected
                
            print(">>", self.voice_data.lower()) # print what you said
            self.voice_data = self.voice_data.lower()
            
            return self.voice_data.lower()
        
    def engine_speak(self, audio_strig):
        audio_strig = str(audio_strig)
        tts = gTTS(text=audio_strig, lang='en')
        r = random.randint(1,20000)
        audio_file =  'audio'+ str(r)+'.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(self.assist_name+':', audio_strig)
        os.remove(audio_file)
        
        
    def theres_exist(self, terms):
        """
        Function for identify if exists the term
        """
        for term in terms:
            if term in self.voice_data:
                return True
            
            
    def respond(self, voice_data):
        if self.theres_exist(['hey', 'hi', 'hello', 'oi', 'holla', 'salve']):
            greetings = [f'Hi {self.person}, what are we doing today?',
                         'Hi Boss, how can I help you',
                         'Hi Boss, what do you need?']
            
            greet = greetings[random.randint(0, len(greetings)-1)]
            self.engine_speak(greet)
          
        #google    
        if self.theres_exist(['find for']) and 'youtube' not in voice_data:
            search_term = voice_data.split("for")[-1]
            url = "http://google.com/search?q=" + search_term
            webbrowser.get().open(url)
            self.engine_speak("here is what I found for" + search_term + ' on google')
            
        #youtube
        if self.theres_exist(["find youtube for"]):
            search_term = voice_data.split("for")[-1]
            url = "http://www.youtube.com/results?search_query=" + search_term
            webbrowser.get().open(url)
            self.engine_speak("here is what I found for" + search_term + 'on youtube')
            
            
            
            
assistent = VirtualAssist('Agata', 'Joao')

while True:
    
    voice_data = assistent.record_audio('listening...')
    assistent.respond(voice_data)
    
    if assistent.theres_exist(['bye', 'goodbye', 'seeyou', 'see you later', 'see you', "it's only for today"]):
        assistent.engine_speak("Have a nice day! Good bye!")
        break
            
