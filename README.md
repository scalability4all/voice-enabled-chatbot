# voice-enabled-chatbot

Implementing a voice enabled chatbot which converses with a user via their voice in natural language. The user should be able to interact with the application like a voice assistant and appropriate responses should be returned by the application (also through voice). The number of topics to converse upon will be fixed however the user should be able to converse through natural language.

If we have topics like the weather, location information, inventory information etc the
application should be able to converse in that particular topic. Like, if we have questions
such as:-

Hey, what is the weather today? - **Weather Information**

I want to know if there are any shopping stores near me. - **Location Information**

Will it rain today? - **Weather Information**

Can you tell me availability of item in Store X? - **Inventory Information**

Initially the application should be able to identify each particular topic and then return the
appropriate response. After that, the chatbot should carry on the conversation regarding that
particular topic. For ex:

**User** - I want to know if there are any shopping stores near me.

**Chatbot** - These are the nearest stores:- A, B, C. Where do you wanna go?

**User** - I want to go to the most popular one among them

**Chatbot**- All right, showing you directions to C.

So, mainly the chatbot should formulate appropriate responses to incoming questions and
carry on the conversation. Keeping in mind, the conversation would be in natural language
and the user is returned sufficient information.


## Concept

Before starting Conversation, bot will fetch the location of the user and other details to give personalized results.

**Step 1: Speech-2-Text:**  Given a speech through Microphone, Store it and Convert it using SpeechRecognition and PyAudio.

**Step 2: Topic Modelling:** Get Entity and Intent of chat using model with a corpora. To get the trained model, we will use the classifier to categorize it to weather, location and inventory. After that using RASA-NLU with Spacy library, we will get the entities.

**Step 3:**  After Finding Intent and Entity, we will set model in following method:
Intent  = Weather: Based on entity specified, We will use weather API to get data about location.
Intent = Location: Following Conversation flow:
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
`python main.py`

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

## Compiling Project for Development or Installation

- Clone the repo by `git clone https://github.com/satyammittal/voice-enabled-chatbot.git` or use ssh.
- `cd` into the cloned repo.
- `sudo apt-get install portaudio19-dev` and `pip install -r requirements.txt` 

## Improvements Planned

1. Completing chat bot so that it works on multiple domain specified through config.
2. Adding classification techniques for intent seperation.
3. Automated method for Entity creation from sentences.
4. Use cache mechanism to give result about recently used query.
5. At the end, the deliverable will be to implement user interface for a sample chatbot implemented.
6. We will also extend it to create plugin for companies requiring chatbot. They can put their domain in config file and data separately to give personalized result.
7. Multi Language Support

## Example

<p align="center">
  <img src="https://i.imgur.com/SPCAW5q.gif" alt="Chat-Sample">
</p>

## References

References Using:

         a) https://medium.com/@rahulvaish/speech-to-text-python-77b510f06de
         
         b) https://link.springer.com/content/pdf/10.1007%2F978-3-642-36973-5_88.pdf
