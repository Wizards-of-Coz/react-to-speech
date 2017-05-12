# Cozmo Reacts to Speech
## Project Description
This is a linear experience about evaluating speech as a form of Input to Cozmo. Players can call out to cozmo and he will look for your face to begin interacting with you. He will analyse your speech and react accordingly. For example, “I hate you” evokes sad emotions from cozmo and saying “I’m sorry” or “I’ve missed you” makes him happy.

## Video
https://www.youtube.com/watch?v=oH928CbpIqM

## Implementation Details
Cozmo SDK’s “cozmo.behavior.BehaviorTypes.FindFaces” is used when the user calls out “Cozmo” or “Buddy” to start the experience. He looks for a face and when he finds one, he starts listening for speech input. Python’s Speech Recognition library is used to process player speech input. The processed speech is sent to Python’s NLP Toolkit that analyzes the sentence based on a training data set and classifies it into a positive or negative emotion (a fraction between -1 and 1). Based on this, Cozmo reacts with an appropriate animation.

## Instructions
### Installation
1. There are dependencies on other Python packages. Install them using pip. 
2. Speech Recognition Library ( pip3 install SpeechRecognition )
3. Natural Language Processing Toolkit ( pip3 install nltk )
4. TextBlob ( pip3 install TextBlob )
5. Common - ( Download it from https://github.com/Wizards-of-Coz/Common )

### Experience
This is a linear experience and requires certain inputs from the user to go through the entire experience.
Call out to Cozmo with the words ‘Cozmo’ or ‘Buddy’. This starts the experience and Cozmo will look for your face. After Cozmo finds a face, he listens for player speech input. Players can now say things to Cozmo and he will react accordingly.

The accuracy of cozmo’s reactions to players’ speech depends on the training data set that is provided. The ‘train’ variable on line 29 is a list of tuples that provides the base for the sentiment analysis. The better this data is, the better the analysis is.

## Thoughts for the Future
The vision of this prototype was to make Cozmo react intelligently to player inputs. Though Speech input might not work so well with Cozmo because he doesn’t have a microphone, this opens up possibilities of adding a lot of character into Cozmo. Cozmo could have an emotion meter that could change with time, that would affect his reactions to things. For example, if Cozmo is already in a bad mood, he would frown at everything. This could be extended to a personality matrix for cozmo where users could, from a UI in the app, select a particular personality for their cozmo and he would behave appropriately.
