from django.shortcuts import render
from django.http import HttpResponse, response
from django.views.decorators.csrf import csrf_exempt

import os, csv, json
# from pprint import pprint

from api.LineMessage import LineMessage

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./api/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Create your views here.
def index(request):
    
    # doc = db.collection(u'Stores').document('Hajiban').get()
    docs = db.collection(u'Stores').where(u'GEO.latitude', u'>', 10).get()

    # docs = getByName('PepperLunch')
    # docs = docs.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

    return HttpResponse(f'{doc.id} => {doc.to_dict()}')

def create(request):
    # csvFilePath = './api/stores/dintaifung.csv'
    # jsonFilePath = './api/stores/dintaifung.json'

    # # read csv file and add to data
    # data = {}
    # with open(csvFilePath) as csvFile:
    #     csvReader = csv.DictReader(csvFile)
    #     for rows in csvReader:
    #         id = rows['id']
    #         data[id] = rows
    # with open(jsonFilePath, 'w') as jsonFile:
    #     jsonFile.write(json.dumps(data, indent=4))

    for filename in os.listdir('./api/stores/'):
        if filename.endswith('.json'):
            collectionName = filename.split('.')[0] # filename minus ext will be used as collection name
            f = open('./api/stores/' + filename, 'r')
            docs = json.loads(f.read())
            # with open('./api/stores/' + filename) as json_data:
            #     docs = json.load(json_data)
            #     pprint(docs)

            print(docs)
            for doc in docs:
                print(doc)
                # db.collection(u'Stores').document(u'Dintaifung').set(doc)

    print('success')
    return HttpResponse('success')

@csrf_exempt
def lineMessage(request):
    print(request)

    # required 'user token id'
    reply_token = 'Ua9fa604e9bdfbd4d1e4fd61b2ba92402'
    
    messages = [
        {
            'type': 'text',
            'text': 'Hi, Im boknoi. \nTEST'
        }
    ]

    print(messages)
    
    line_message = LineMessage(messages)
    line_message.reply(reply_token)
    
    return HttpResponse('success')