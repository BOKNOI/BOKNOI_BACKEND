from unicodedata import name
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

# Recieving request
@csrf_exempt
def findStoreByName(request):
    body = request.body.decode('utf-8') 
    data = json.loads(body)

    # 1. recieve GPS and picture
    print(data['name'], data['gps'])

    # 2. get Store
    docs = db.collection(u'Stores').where(u'name', u'in', data['name']).get()

    # docs = getByName('PepperLunch')
    # docs = docs.stream()

    temp = {'name': [], 'detail': []}
    
    for doc in docs:
        # print(f'{doc.id} => {doc.to_dict()} \n')
        temp['name'].append(doc.id)
        temp['detail'].append(doc.to_dict())

    print(temp['name'])

    # 3. send data to ALGORITHM
    # lineMessage(data['id'])

    return HttpResponse('OK -- findStore')

@csrf_exempt
def findStoreByPicture(request):
    body = request.body.decode('utf-8') 
    data = json.loads(body)
    print(data['id'])

    # 1. recieve GPS and picture

    # 2. get all Store [*, pictures]

    # 3. send data to ALGORITHM
    lineMessage(data['id'])

    return HttpResponse('OK -- findStore')

# Sending store detail
def getStore(request):
    print(request.GET.get('id'))

    # 1. recieve param (store name[id])
    id = request.GET.get('id')

    # 2. get store from DB
    doc = db.collection(u'Stores').document(id).get()
    data = doc.to_dict()

    print(type(data))
    data = json.dumps(data)
    print(type(data))

    # 3. send data
    return HttpResponse(f'{ data }')

# Sending LINE message
@csrf_exempt
def lineMessage(request):
    print(request)

    # required 'user token id'
    reply_token = request
    
    messages = [
        {
            "type": "flex",
            "altText": "this is a flex message",
            "contents": {
                "type": "bubble",
                "size": "giga",
                "direction": "ltr",
                "action": {
                    "type": "uri",
                    "label": "https://boknoi.web.app/store",
                    "uri": "https://boknoi.web.app/store"
                },
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",

                            "text": "Hachiban ramen", 

                            "weight": "bold",
                            "size": "xxl",
                            "color": "#1B1B1BFF",
                            "align": "center",
                            "gravity": "top",
                            "margin": "none",
                            "wrap": True,

                            "action": {
                            "type": "uri",
                            "uri": "https://boknoi.web.app/store"
                            },

                            "contents": []
                        }
                    ]
                },
                "hero": {
                    "type": "image",

                    "url": "https://img.wongnai.com/p/1920x0/2016/10/31/97eb0ae9bf0848f786ce043d970dfca6.jpg",

                    "size": "full",
                    "aspectRatio": "1.51:1",
                    "aspectMode": "cover",
                    "backgroundColor": "#FFFFFFFF"
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                            {
                                "type": "button",
                                "action": {
                                "type": "uri",
                                "label": "ดูข้อมูลเพิ่มเติม",

                                "uri": "https://boknoi.web.app/store"
                                },
                            }
                        ]
                }
            }
        }
    ]

    # print(messages)
    
    line_message = LineMessage(messages)
    line_message.reply(reply_token)
    
    return HttpResponse('success')

# -------------------- TEST --------------------

def index(request):
    print(request)

    # doc = db.collection(u'Stores').document('Hajiban').get()
    docs = db.collection(u'Stores').where(u'GEO.latitude', u'>', 10).get()

    # docs = getByName('PepperLunch')
    # docs = docs.stream()

    temp = {'name': [], 'detail': []}
    
    for doc in docs:
        # print(f'{doc.id} => {doc.to_dict()} \n')
        temp['name'].append(doc.id)
        temp['detail'].append(doc.to_dict())

    print(temp)

    return HttpResponse(temp['name'])

def create(request):
    print(request)
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

    # for filename in os.listdir('./api/stores/'):
        # f = open('./api/stores/result.json')
        # docs = json.loads(f.read())

    with open('./api/stores/result.json', encoding="utf8") as json_data:
        docs = json.load(json_data)


    print(range(len(docs)))
    print('---')

    for i in range(len(docs)):
        name = docs[i]['name']
        print(name)
        db.collection(u'Stores').document(name).set(docs[i])
            # print(doc)


        # for doc in docs:
        #     print(doc)

    # if filename.endswith('.json'):
    #     collectionName = filename.split('.')[0] # filename minus ext will be used as collection name
    #     f = open('./api/stores/' + filename, 'r')
    #     docs = json.loads(f.read())
    with open('./api/stores/dintaifung.json') as json_data:
        docs = json.load(json_data)
        # pprint(docs)

    # print(docs)
    # for doc in docs:
    #     print(doc)
    #     print('\n')
    #     # db.collection(u'Stores').document(u'Dintaifung').set(doc)
            

    print('success')
    return HttpResponse('success')

