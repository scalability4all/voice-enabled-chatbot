import config
import models
import pyttsx3
import crud


def speak(text):
    talk.say(text)
    talk.runAndWait()


def checkIfNull(field, inp):
    while inp == "":
        print("{} should not be empty. Please type some username".format(field))
        speak("{} should not be empty. Please type some username".format(field))
        inp = input()
    return inp


talk = pyttsx3.init()
voices = talk.getProperty('voices')
talk.setProperty('voice', voices[1].id)
volume = talk.getProperty('volume')
talk.setProperty('volume', 10.0)
rate = talk.getProperty('rate')
talk.setProperty('rate', rate - 25)
# creating object to isert data into table
obj = crud.crudOps()
print("Welcome to Website")
speak("Welcome to Website")
print("Register")
speak("Register")
formFields = config.form_fields
lenFields = len(formFields)
tableRow = []

# primary key
print("Could you type a user{}".format(formFields[0]['fname']))
speak("Could you type a user{}".format(formFields[0]['fname']))
userfield = input()

# check if it is null
userfield = checkIfNull(formFields[0]['fname'], userfield)

# Check if it is already exists
primarycol = obj.primaryCol()
while userfield in primarycol:
    print("Sorry Username already exists type another username")
    speak("Sorry Username already exists type another username")
    userfield = input()
tableRow.append(userfield)

# For remaining form fields
for i in range(1, lenFields):
    print("Could you type your {}".format(formFields[i]['fname']))
    speak("Could you type your {}".format(formFields[i]['fname']))
    userfield = input()
    # check if it is null
    if not formFields[i]['null']:
        userfield = checkIfNull(formFields[i]['fname'], userfield)
    tableRow.append(userfield)

newRow = models.Register(
    col1=tableRow[0],
    col2=tableRow[1],
    col3=int(tableRow[2]),
)
obj.insertRow(newRow)
getData = obj.allRow()
print(getData)
