import kivy
from kivymd.app import MDApp
from kivymd.uix.screenmanager  import ScreenManager
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDIcon
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivy.core.text import LabelBase
from kivy.properties import StringProperty,NumericProperty


Window.size = (350,550)

class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "KeepCalm-Medium.ttf"
    font_size = 17

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name="KeepCalm-Medium.ttf"
    font_size = 17
    
    
class Jarvis(MDApp):
    
    def change_screen(self,name):
        screen_manager.current = name
    
    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        #label = MDIcon(icon="robot",pos_hint={"center_x":0.5,"center_y":0.9})
        #btn = MDIconButton(icon = "microphone",pos_hint={"center_x":0.5,"center_y":0.2},icon_size="64sp",on_release=self.start)
        screen_manager.add_widget(Builder.load_file("Main.kv")) 
        screen_manager.add_widget(Builder.load_file("Chats.kv"))
       
        return screen_manager
    
    def start(self):
        #screen_manager.get_screen('chats').chat_list.add_widget(Command(text="Hello",size_hint_x=.2,halign="center"))
        #===================================Functions=====================================================
        import speech_recognition as sr
        import pyttsx3
        import pywhatkit
        import datetime
        import wikipedia
        import urllib
        import pyaudio
        import random
        import re
        import wolframalpha
        import time


        # =================================================In Memory===================================================
        GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
                    "ok jarvis", "are you there","hi jarvis"]

        GREETINGS_RES = ["Always there for you, Sir", "I am ready sir","Your wish, My command", "How can I help you Sir?", "I am online and ready, Sir"]

        POS_REPLY = ["i am fine", "doing good"]

        REPLIES = [
                    'play',                       #0
                    'time',                       #1
                    'date',                       #2
                    'who is',                     #3
                    'calculate',                  #4
                    'search',                     #5
                    'search for',                 #6
                    'what is the day today',      #7
                    'what is',                    #8
                    'which day is today',         #9
                    'day today',                  #10
                    'nothing',                    #11
                    'no',                         #12 
                    'stop',                       #13
                    'exit'                        #14
                    'how are you'                 #15
                    'who are you'                 #16
                    ]

        #================================================Pre-defined Variables==========================================                 

        engine = pyttsx3.init()
        listener = sr.Recognizer()

        #================================================Defined Functions================================================
        def talk(text):
            if len(text) < 6 :
                size = .22
            
            elif len(text) < 11:
                size = .32
            
            elif len(text) < 16:
                size = .45
            
            elif len(text) <  21:
               size = .58
            
            elif len(text) < 26:
                size = .71
            
            else :
                size = .77
            halign = "left"
            
            screen_manager.get_screen('chats').chat_list.add_widget(Command(text=text,size_hint_x=size,halign=halign))
            engine.say(text)
            print(text)            
            engine.runAndWait()


        def take_cmd():
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    voice = listener.listen(source, phrase_time_limit=5, timeout=1)
                    command = listener.recognize_google(voice,language="en-US")
                    command = command.lower()
                    if len(command) < 6 :
                        size = .22
             
                    elif len(command) < 11:
                        size = .32
             
                    elif len(command) < 16:
                        size = .45
             
                    elif len(command) <  21:
                        size = .58
             
                    elif len(command) < 26:
                        size = .71
             
                    else :
                        size = .77
                    halign = "left"
                    
                    screen_manager.get_screen('chats').chat_list.add_widget(Response(text=command,size_hint_x=size,halign=halign))

                    print(command)
                    Jarvis_search(command)
                    #screen_manager.get_screen('chats').chat_list.add_widget(Command(text=command,size_hint_x=.2,halign="center"))
                    return command
                    
            except:
                pass


        def comnd_jarvis():
            
            command = take_cmd()
            
            if('jarvis' in command):
                
                print(command)
                return command

            else:
                print("Usage: Jarvis...")
                exit(0)


        def check(string, reply):
            if (reply in string):
                return(1)

            else: return(0) 

        #Play on Youtube
        def play(command):
            song = command.replace('play', '') 
            talk("Playing " + song)
            pywhatkit.playonyt(song)
            exit(0)
            return False

        # Time
        def timenow():
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk("Current Time is " + time)
            talk("Anything else sir")
            return True

        # Date
        def datenow():
            date = datetime.date.today().strftime('%d %b, %Y')
            talk(date)
            talk("Anything else sir")
            return True

        # Who is?
        def who(command):
            person = command.replace('who is', '') 
            info = wikipedia.summary(person, 2)
            talk(info)
            talk("Anything else?")
            return True

        # Calculate
        def calculate(question):
            try:
                client = wolframalpha.Client("chris.kurian.btech2022@sitpune.edu.in")
                answer = client.query(question)
                answer = next(answer.results).text
                talk(answer)
                return True
            except:
                talk("Sorry sir I couldn't fetch your question's answer. Please try again ")
                return True

        # Search in Wiki
        def search(command):
            sch = command.replace('search', '') or command.replace('search for', '') or command.replace('what is', '')
            srch_result = wikipedia.summary(sch, 2)
            talk(srch_result)
            talk("Anything else?")
            return True

        # Day Today
        def day():
            date = datetime.date.today().strftime('%d %m %Y')
            day_today = datetime.datetime.today().strptime(date, '%d %m %Y').weekday()
            day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            talk("Today is " + day_name[day_today])
            talk("What do you like to do today?")
            return True

        # How are you?
        def how_are_u():
            talk("I am Fine Sir, Thanks For Asking!")    
            talk("How are you, sir?")
            return True

        # Self intro 
        def self_intro():
            talk("I am Jarvis, your virtual assistant")
            talk("What can I do for you?")
            return True
                



                
        # =====================================MAIN SEARCH====================================

        def Jarvis_search(rep):

            if (rep in GREETINGS):
                talk(random.choice(GREETINGS_RES))
                return True

            if (check(POS_REPLY, rep) == 1):
                talk("Thats nice")
                talk("How can I help you today?")
                return True
            
            
            command_num = 0

            for i in range(16):
                if REPLIES[i] in rep:
                    command_num = i
                    break

            if command_num == 0:
                play(rep)

            elif command_num == 1:
                timenow()  

            elif command_num == 2:
                datenow()

            elif command_num == 3:
                who(rep)

            elif command_num == 4:
                calculate(rep)

            elif command_num == 5 or command_num == 6 or command_num ==8:
                search(rep)

            elif command_num == 7 or command_num == 9 or command_num == 10:
                day()

            elif command_num == 11 or command_num == 12 or command_num == 13 or command_num == 14:
                talk("Thank You!")
                return False
            
            elif command_num == 15:
                return how_are_u()

            elif command_num == 16:
                return self_intro()
        #=================================================Start From Jarvis==============================================
    
        #cmd = comnd_jarvis()


        
        command = take_cmd()


        
if __name__ == "__main__":
    LabelBase.register(name="Heva",fn_regular="DS-DIGIT.TTF")
    Jarvis().run()