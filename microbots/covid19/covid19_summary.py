import urllib.request
import os.path
import zipfile
import pathlib
import json

print('COVID-19: a summary of new and total cases per country updated daily.')

# Create a directory if it does not exist 
filesDir = 'files'
if not os.path.exists(filesDir):
    os.makedirs(filesDir)

# Defines functions and classes which help in opening URLs (mostly HTTP) in a complex world
# Retrieves the contents of url and places it in filename.
endPointUrl = 'https://api.covid19api.com/summary'
jsonFileName = 'summary.json'
zipFileName = 'summary.zip'

# relativeJsonFilePath = os.path.join(filesPath, jsonFileName)
relativeZipFilePath = os.path.join(filesDir, zipFileName)

# Request and write Json file
urllib.request.urlretrieve(endPointUrl, jsonFileName)

# Create a ziped file of files in file folder and name it with the date
zipObj = zipfile.ZipFile(relativeZipFilePath, mode='w')
zipObj.write(jsonFileName)
zipObj.close()

# Delete json file
os.remove(jsonFileName)
