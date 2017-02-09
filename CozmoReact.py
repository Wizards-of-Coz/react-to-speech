import asyncio
import cozmo
from Common.woc import WOC
from Common.colors import Colors
import speech_recognition as sr
from os import system
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from nltk.corpus import movie_reviews
import random
import _thread
import traceback

'''
Cozmo Reactions Module
@class CozmoReact
@author - Team Wizards of Coz
'''
class CozmoReact(WOC):
    
    reactionDict = {"happy" : {"emo":['anim_memorymatch_successhand_cozmo_02','anim_memorymatch_successhand_player_02','anim_rtpkeepaway_playeryes_03','anim_rtpkeepaway_playeryes_02','anim_sparking_success_01','anim_reacttoblock_ask_01','anim_reacttoblock_happydetermined_02']},
                    "very_happy":{'emo':['anim_memorymatch_successhand_cozmo_03','anim_memorymatch_successhand_cozmo_04']},
                    "sad":{'emo':['anim_driving_upset_start_01','anim_memorymatch_failgame_cozmo_03','anim_keepaway_losegame_02']},
                    "angry":{'emo':['anim_bored_01','anim_bored_02','anim_keepaway_losegame_03','anim_keepaway_losehand_03','anim_speedtap_lookatplayer','anim_reacttoblock_frustrated_01','anim_reacttoblock_frustrated_int2_01']},
                    "idle":{'emo':['anim_sparking_idle_03']},
                    "bored":{'emo':['anim_bored_01','anim_bored_02','anim_bored_event_01','anim_bored_event_02','anim_bored_event_04']}}
            
    
    train = [
        ('Hi Cosmos','happy'),
        ('Hi-5','happy'),
        ('Hey buddy','happy'),    
        ('I had a great evening', 'happy'),
        ("I'm leaving him", 'sad'),
        ("Get lost", 'sad'),
        ("Bye",'sad'),
        ('I love this sandwich.', 'happy'),
        ('This is an amazing place!', 'happy'),
        ('I feel very good about these beers.', 'happy'),
        ('This is my best work.', 'happy'),
        ("What an awesome view", 'happy'),
        ('I do not like this restaurant', 'sad'),
        ('I am tired of this stuff.', 'sad'),
        ("I can't deal with this", 'sad'),
        ('He is my sworn enemy!', 'sad'),
        ('My boss is horrible.', 'sad'),
        ('You are grounded', 'sad'),
        ('You have been bad', 'sad'),
        ('I hate working late.', 'sad'),
        ('I had a very bad day.', 'sad'),
        ('The dinner was horrible', 'sad'),
        ("I don't want to play with you", 'sad'),
        ("I missed you", 'happy'),
        ("I miss you", 'happy'),
        ('you suck', 'sad'),
        ('I love you', 'happy'),
        ('I like you', 'happy'),
        ('I hate you', 'sad'),
        ('U suck', 'sad'),
        ('idontlikeyou', 'sad'),
        ("I'm sorry", 'happy'),
        ("I'll be back soon", 'happy'),
        ("You are a good boy", 'happy'),
    ]
    
    cl = None
    reaction = None
    exit_flag = False
    lookingForFace = False
    face = None
    cubes = None
    audioThread = None
    lookThread = None
    emotionScale = 0
    
    
    
    def __init__(self, *a, **kw):
        
        self.cl = NaiveBayesClassifier(self.train)
        cozmo.setup_basic_logging()
        cozmo.connect(self.startResponding)
        
        
        
    def startResponding(self, coz_conn):
        asyncio.set_event_loop(coz_conn._loop)
        self.coz = coz_conn.wait_for_robot()
        self.coz.enable_facial_expression_estimation = True
        self.coz.enable_reactionary_behaviors = True
        
        self.audioThread = _thread.start_new_thread(self.startAudioThread, ())
        
        self.coz.world.add_event_handler(cozmo.objects.EvtObjectAppeared, self.foundCube)
        
        while not self.exit_flag:
            asyncio.sleep(0)
        self.coz.abort_all_actions()
    
    
    
    def startAudioThread(self):
        try:
            print("Take input");
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.startListening())
        except:
            print("Audio Thread Exception")
    
    
    
    async def startListening(self):
        if not self.lookingForFace:
            print("Taking input");
            
            r = sr.Recognizer()
            r.energy_threshold = 5000
            print(r.energy_threshold)
            with sr.Microphone(chunk_size=512) as source:
                audio = r.listen(source)
    
            try:
                speechOutput = r.recognize_google(audio)
                self.processSpeech(speechOutput);
                await asyncio.sleep(1);
                await self.startListening()
    
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                self.coz.play_anim("anim_explorer_huh_01_head_angle_40").wait_for_completed()
                self.react('idle')
                await asyncio.sleep(0);
                await self.startListening()
    
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    
    
    def processSpeech(self,speechOutput):
        print(speechOutput)
        if self.face is None:
            if 'cozmo' in speechOutput or 'Cozmo' in speechOutput or 'Cosmo' in speechOutput or 'buddy' in speechOutput or 'body' in speechOutput or 'osmo' in speechOutput or 'Kosmos' in speechOutput or 'Kosmo' in speechOutput:
                self.lookingForFace = True
                self.lookForFace()
        else:
            print(speechOutput + " " + self.classifyText(speechOutput))
            emotion = self.classifyText(speechOutput)
            self.react(emotion)
            
            
            
    def lookForFace(self):
        find_face = self.coz.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)
        try:
            self.face = self.coz.world.wait_for_observed_face(timeout=10)
            print("Found a face!", self.face)
        except asyncio.TimeoutError:
            find_face.stop()
            self.coz.say_text("I can't find you").wait_for_completed()
            self.emotionScale -= 0.1
            if self.emotionScale <= -0.3 :
                self.coz.play_anim("anim_gotosleep_fallasleep_01").wait_for_completed()
            else:
                self.react("bored")
            self.lookingForFace = False
        finally:
            find_face.stop()
            if self.face is not None:
                self.coz.play_anim("anim_greeting_happy_01").wait_for_completed()
                self.emotionScale = 0
                self.lookingForFace = False
                
     
     
    def react(self,emotion):
        self.coz.play_anim(random.choice(self.reactionDict[emotion]["emo"])).wait_for_completed()
        

        
    def classifyText(self,speechOutput):
        sentence = TextBlob(speechOutput, classifier=self.cl)
        return sentence.classify()
    
    
    
    def foundCube(self, event, *, image_box, obj, pose, updated, **kw):
        self.react("happy")
    
    
    
    def flash_backpack(self, flag):
        self.coz.set_all_backpack_lights(cozmo.lights.green_light.flash() if flag else cozmo.lights.off_light)


if __name__ == '__main__':
    CozmoReact()