# Voice Enabled Chatbot- one of the best

[![Build Status](https://travis-ci.org/scalability4all/voice-enabled-chatbot.svg?branch=master)](https://travis-ci.org/scalability4all/voice-enabled-chatbot) [![codecov](https://codecov.io/gh/scalability4all/voice-enabled-chatbot/branch/master/graph/badge.svg)](https://codecov.io/gh/scalability4all/voice-enabled-chatbot)

Implementing a voice enabled chatbot which converses with a user via their voice in natural language. The user should be able to interact with the application like a voice assistant and appropriate response will be returned by the application (also through voice). The number of topics to converse upon will be fixed however the user should be able to converse through natural language.

If we have topics like the weather, location information, inventory information etc the
application should be able to converse in that particular topic. Like, if we have questions
such as:-

Hey, what is the weather today? - **Weather Information**

I want to know if there are any shopping stores near me? - **Location Information**

Will it rain today? - **Weather Information**

Can you tell me availability of item in store X? - **Inventory Information**

Initially the application should be able to identify each particular topic and then return the
appropriate response. After that, the chatbot should carry on the conversation regarding that
particular topic. For eg:

**User** - I want to know if there are any shopping stores near me.

**Chatbot** - These are the nearest stores:- A, B, C. Where do you wanna go?

**User** - I want to go to the most popular one among them

**Chatbot**- All right, showing you directions to C.

So, mainly the chatbot should formulate appropriate responses to incoming questions and
carry on the conversation. Keep in mind, the conversation would be in natural language
and the user has returned sufficient information.


## Concept

Before starting conversation, bot will fetch the location of the user and other details to give personalized results.

**Step 1: Speech-2-Text:**  Given a speech through Microphone, store it and convert it using SpeechRecognition and PyAudio libraries.

**Step 2: Topic Modelling:** Get Entity and Intent of chat using model with a corpora. To get the trained model, we will use the classifier to categorize it into weather, location and inventory. After that using RASA-NLU with Spacy library, we will extract the entities.

**Step 3:**  After Finding Intent and Entity, we will set the model using the following method:
Intent  = Weather: Based on entity specified, We will use weather API to fetch data of location.
Intent = Location: Following conversation flow:
Get Stores located or Any Nearby Stores
Choose Store
Inventory Details about Store

**Step 4:** Use cache mechanism to give result about recently used query.

## Changelog
- #### v0.1.1
    - Added support for speech to text
    - Added support of weather and google places api
    - Added basic introduction chat
    - Added voice support to chat

## Usage

To change the language, enter the BCP-47 code from [language support](https://cloud.google.com/speech-to-text/docs/languages). If you want the language to be English (default), press enter.

Arguments:
```
         For now, you can use it for following domain:
         Introduction: Hi, Hello..
         Weather: Get weather info
         Google Search: get any google search
         Wikipedia Search: What is "query"?
         Google Places: Get me best places.
```
You can quit by pressing <kbd>Ctrl</kbd>+<kbd>C</kbd>

## Build the application locally
* Clone the repo
    - Clone the ```voice-enabled-chatbot``` repo locally. In the terminal, run : <br>
    ```git clone https://github.com/satyammittal/voice-enabled-chatbot.git```
* Install the dependencies
    - We need PyAudio, a cross-platform audio I/O library.For this run : <br>
    ```sudo apt-get install portaudio19-dev``` (linux) <br>
    ```brew install portaudio``` (mac) <br>
    - Further, install other requirements using : <br>
    ```pip install -r requirements.txt``` <br>
    - Using windows, install other requirements using: <br>
    ```pip install -r requirements_windows.txt```<br>
    - Install english stopwords using : <br>
    ```python -c "import nltk; nltk.download('stopwords')"``` <br>
    - The *pyowm* is supposed to be instable in windows. <br>
* Configure Google API Key
    - Go to the [Google Cloud Platform Console](https://cloud.google.com/console/google/maps-apis/overview).
    - Select or create the project for which you want to add an API key.
    - Click the menu button and select __APIs & Services > Credentials__.
    - On the __Credentials__ page, click __Create credentials > API key__.
    - Copy and paste the API key in [`config.py`](/config.py) file.
    
## Run the application 
Run the application using command - ```python chatbot.py```

## Milestones

1. Completing chat bot so that it works on multiple domain specified through config.
2. Adding classification techniques for intent seperation.
3. Automated method for Entity creation from sentences.
4. Use cache mechanism to give result about recently used query.
5. At the end, the deliverable will be to implement user interface for a sample chatbot implemented.
6. We will also extend it to create plugin for companies requiring chatbot. They can put their domain in config file and data separately to give personalized result.
7. Multi Language Support

## Sample output

<p align="center">
  <img src="https://i.imgur.com/SPCAW5q.gif" alt="Chat-Sample">
</p>

## References
* [Speech To Text - Python](https://medium.com/@rahulvaish/speech-to-text-python-77b510f06de)
* [Topic-Focused Summarization of Chat Conversations](https://link.springer.com/content/pdf/10.1007%2F978-3-642-36973-5_88.pdf)
