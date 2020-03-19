# FaceFilter Microbot
When users identified as in "strong moods", even intelligent replies are not always very effective. A creative response that can possibly alter their strong mood positively showing them their Face with filter that is relevant to situation in the conversation.

Lets see in action sample conversations.

<table>
  <tr>
    <td width="30%"><img src="https://i.ibb.co/M9k62Yv/demo-cute.png" alt="Chat-Sample"></td>
    <td width="70%">As you can see in the conversation, user has 'strong mood' of being sad because of not looking good. Our mood detection detects this strong signal and our intent classifier calls our bot, and our bot sends this uplifting FaceFilter using users camera.</td>
  </tr>
</table>
<table>
  <tr>
    <td width="70%">Here, user has 'strong mood' of being sad because loneliness. Our mood detection detects this strong signal and our intent classifier calls our bot, and our bot sends this funny FaceFilter to create mystery to take make it fun and lite.</td>
    <td width="30%"><img src="https://i.ibb.co/CQvjCMX/demo-love.png" alt="Chat-Sample"></td>
  </tr>
</table>
<table>
  <tr>
    <td width="30%"><img src="https://i.ibb.co/YZCy7Ly/demo-spaceman.png" alt="Chat-Sample"></td>
    <td width="70%">Here, user has 'strong mood' of passion and adds patience for future. Our mood detection detects this strong signal and our intent classifier calls our bot, and our bot sends breaks that patience by helping user visualize future that he has to be patient for!</td>
  </tr>
</table>

This microbot will be a really cool addition to our chatbot and make it more fun!


## Break Down

So what do we need to make this work? We break down in parts :-

<ul>
  <li> <b> Step 1 - Building Live Filters </b><br>
        - Live Face detection contour <br>
        - Image processing to create photos for each variety of filters <br>
        - Stitching corresponding image on detected contour points <Br>
  </li>
  <li> <b>Step 2 - Mood Classification Module </b> </li>
  <li> <b>Step 3 - Training Params for Intent Classifier </b> </li>
  <li> <b>Step 4 - Integrating and creating configuration file </b> </li>
</ul>

## Changelog
- #### v0.1.1
    - Added demo/readme

## Usage
`python main.py`


## Build the application locally
Will be updated
<!--* Clone the repo
    - Clone the ```voice-enabled-chatbot``` repo locally. In the terminal, run : <br>
    ```git clone https://github.com/satyammittal/voice-enabled-chatbot.git```
* Install the dependencies
    - We need PyAudio, a cross-platform audio I/O library.For this run : <br>
    ```sudo apt-get install portaudio19-dev```
    - Further, install other requirements using : <br>
    ```pip install -r requirements.txt```-->
## Run the application 
Will be updated <!--Run the application using command - ```python chatbot.py```-->

