import requests
import argparse
import pprint
import json
import time

"""
requirements

pip install requests
pip install argparse
pip install pprint
pip install json
pip install time
"""

ipInformation= {'ipInformation':{
                'geographyData':{},
                'downloadContents':{}}}

def addNewValue(jsonObject, key, value):
    if key in jsonObject:
        if not isinstance(jsonObject[key], list):
            jsonObject[key] = [jsonObject[key]]
        jsonObject[key].append(value)
    else:
        jsonObject[key] = value

def downloadSearch(apiKEY, searchIP, requestURL):
    lastURL= f'{ipURL}{searchIP}&days=30&contents=100&key={apiKEY}'
    requestData= json.loads(requests.get(lastURL).content.decode('utf-8'))

    #infoForIP
    ipInformation['ipInformation']['ip']= requestData['ip']
    ipInformation['ipInformation']['internetServiceProvider']= requestData['isp']
    ipInformation['ipInformation']['sexualyContent']= 'False' if requestData['hasPorno'] or requestData['hasChildPorno']== 'False' else 'True'
    ipInformation['ipInformation']['geographyData']['country']= requestData['geoData']['country']
    ipInformation['ipInformation']['geographyData']['city']= requestData['geoData']['city']

    #downloadContentInfo
    for allData in requestData['contents']:
        addNewValue(ipInformation['ipInformation']['downloadContents'], 'category', allData['category'])
        addNewValue(ipInformation['ipInformation']['downloadContents'], 'downloadItemName', allData['name'])

    print('\n')  
    pprint.pprint(ipInformation)
    

def ipExist(apiKEY, ipAddr, requestURL):
        lastURL= f'{requestURL}{ipAddr}&key={apiKEY}'
        requestData= json.loads(requests.get(lastURL).content.decode('utf-8'))

        if requestData['exists']== True:
            print(f'yep \'{ipAddr}\' found.')
        else:
            print(f'nope \'{ipAddr}\' not found.:|')

apiKEY= '5b26f6e5014f4a68b6e8c0116220f026' #CHANGE ME!!!!
ipURL= 'https://api.antitor.com/history/peer?ip='
existIPurl= 'https://api.antitor.com/history/exist?ip='

argParse = argparse.ArgumentParser(description='I Know What You Download')
argParse.add_argument('-i','--ipAddress', help='Give ip for search')
argParse.add_argument('-e','--exist', help='Verify if the IP address is in the database')
argParse.add_argument('-if','--ipFile', help='Query the entire IP list')
argParse.add_argument('-ef','--existFile', help='Verify if IP list is in database')
parseAllArgument= vars(argParse.parse_args())

ipAddress= parseAllArgument['ipAddress']
existQuery= parseAllArgument['exist']
ipFile= parseAllArgument['ipFile']
existFile= parseAllArgument['existFile']

if bool(ipAddress)== True:
    downloadSearch(apiKEY, ipAddress, ipURL)

if bool(existQuery)== True:
    ipExist(apiKEY, existQuery, existIPurl)

if bool(ipFile)== True:
    allIP = [ipList.rstrip('\n') for ipList in open(ipFile).readlines()]
    for ip in allIP:
        downloadSearch(apiKEY, ip, ipURL)

if bool(existFile)== True:
    allIP = [ipList.rstrip('\n') for ipList in open(existFile).readlines()]
    for ip in allIP:
        ipExist(apiKEY, ip, existIPurl)
