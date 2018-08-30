import numpy as np
import pandas as pd
from urllib import request
import json
import logging
from recom import approot
from recom.db import oracle_connect
from functools import reduce

logging.basicConfig(level=logging.DEBUG)

ESF_URL = 'http://mapi.house365.com/taofang/v1.0/esf/?method=getHouseListNew&name=HouseSellEX&city=nj&id='


def readCSV(phone):
    deviceid = relation(phone)
    filepath = approot.get_dataset("select_DEVICE_ID_CONTEXT_ID__from_DWB_DA.csv")
    data = pd.read_csv(filepath)
    data.columns = ['deviceId', 'contentId']
    data = data[data['deviceId'] == deviceid]
    return data


def secondHouseRequest(contentIds):
    df = pd.DataFrame(columns=['id', 'price', 'blockname'], dtype=np.int8)
    logging.debug(ESF_URL + contentIds)
    for i in range(0, len(contentIds), 350):
        tempContentIds = contentIds[i:i + 350]
        response = request.urlopen(ESF_URL + tempContentIds)
        response = response.read().decode('utf-8')
        logging.info(response)
        if response != '-1':
            jsonObjects = json.loads(response)
            for i, object in enumerate(jsonObjects):
                df.loc[i] = [object['id'], float(object['price']), object['blockinfo']['blockname']]
    return df


def secondHouseRequest2(contentIds):
    logging.debug(ESF_URL + contentIds)
    resultMap = dict()
    resultMap['cityCenter'] = '{"lat": 32.0647517242,"lng": 118.8029140176}'
    resultMap['poiTotalCount'] = len(contentIds)
    temp_list = list()
    for i in range(0, len(contentIds), 350):
        tempContentIds = contentIds[i:i + 350]
        response = request.urlopen(ESF_URL + tempContentIds)
        response = response.read().decode('utf-8')
        logging.info(response)
        if response != '-1':
            jsonObjects = json.loads(response)
            for object in jsonObjects:
                print(object)
                temp = dict()
                if "lat" not in object["blockinfo"] or object["blockinfo"]["lat"] == "":
                    block = getBlockCoord(object["blockinfo"]["blockname"])
                    if block is None:
                        continue
                    else:
                        temp["lat"] = block["lat"]
                        temp["lng"] = block["lng"]
                else:
                    temp["lat"] = object["blockinfo"]["lat"]
                    temp["lng"] = object["blockinfo"]["lng"]
                temp["averPrice"] = object["averprice"]
                temp["blockName"] = object["blockinfo"]["blockname"]
                temp["buildArea"] = object["buildarea"]
                temp["buildYear"] = object["buildyear"]
                temp["district"] = object["district"]
                temp["fitment"] = object["fitment"]
                temp["floor"] = object["floor"]
                temp["forward"] = object["forward"]
                temp["hall"] = object["hall"]
                temp["houseId"] = object["id"]
                temp["mright"] = object["mright"]
                temp["price"] = object["price"]
                temp["room"] = object["room"]
                temp["streetName"] = object["streetname"]
                temp["toilet"] = object["toilet"]
                temp["totalFloor"] = object["totalfloor"]
                temp_list.append(temp)
    resultMap['pois'] = temp_list
    logging.debug(json.dumps(resultMap, ensure_ascii=False))
    return json.dumps(resultMap, ensure_ascii=False)


def relation(phone):
    relations = dict()
    relations["15077827585"] = "864621038192553"
    relations["13770324189"] = "353460084288793"
    relations["13675189197"] = "865970030389108"
    relations["13601901399"] = "860980031132311"
    relations["17855106781"] = "865970034361434"
    relations["15905175211"] = "866533031935839"
    relations["13390901599"] = "861918034499591"
    relations["15951001888"] = "358520088841320"
    relations["15850780069"] = "869885031905924"
    relations["13851499283"] = "867960033998367"
    relations["13401952869"] = "864284035078679"
    relations["18951603156"] = "A00000751717EE"
    relations["18051082210"] = "867455031299405"
    relations["15295123506"] = "352324072851122"
    relations["15105198373"] = "866318037044764"
    relations["13913993926"] = "863184037700430"
    relations["17302584660"] = "864032031775743"
    relations["18055500055"] = "865032030154899"

    return relations[phone]


def historyDataFrame(response):
    data = pd.DataFrame(columns=['id', 'price', 'blockname'], dtype=np.int8)
    json_respose = json.loads(response)
    for object in json_respose:
        data.append(pd.Series([object['id'], object['price'], object['blockinfo']['blockname']]), ignore_index=True)
    logging.debug(data)
    return data


def get_contentIds(data):
    contentIds = ",".join(data["contentId"])
    logging.debug(contentIds)
    return contentIds


def relative_blocks(blockname):
    relative_block_name = list()
    relativeBlockFile = approot.get_dataset("relativeBlockName.json")
    file = open(relativeBlockFile, 'r', encoding='utf-8')
    jsonObject = json.load(file)
    if blockname in jsonObject.keys():
        for key in jsonObject[blockname]:
            relative_block_name.append(key)
    return relative_block_name


def statistical(df):
    relativeBlocksName = list()
    for name in df['blockname'].unique():
        relativeBlocksName.extend(relative_blocks(name))
    if len(relativeBlocksName) > 0:
        return oracle_connect.get_data(set(relativeBlocksName), df['price'].mean() - 50, df['price'].mean() + 50)
    else:
        return "no relative block name"


def startup(phone):
    data = readCSV(phone)
    contentIds = get_contentIds(data)
    secondHouseData = secondHouseRequest(contentIds)
    if secondHouseData.empty:
        return "no history"
    else:
        return statistical(secondHouseData)


def secondHouseRequestJson(datas):
    data = map(lambda x: str(x[0]), datas)
    URL = ",".join(list(data))
    response = request.urlopen(ESF_URL + URL).read().decode('utf-8')
    json_objects = json.loads(response)
    resultMap = dict()
    resultMap['cityCenter'] = '{"lat": 32.0647517242,"lng": 118.8029140176}'
    resultMap['poiTotalCount'] = 10
    temp_list = list()
    for object in json_objects:
        temp = dict()
        if "lat" not in object["blockinfo"] or object["blockinfo"]["lat"] == "":
            block = getBlockCoord(object["blockinfo"]["blockname"])
            if block is None:
                continue
            else:
                temp["lat"] = block["lat"]
                temp["lng"] = block["lng"]
        else:
            temp["lat"] = object["blockinfo"]["lat"]
            temp["lng"] = object["blockinfo"]["lng"]
        temp["averPrice"] = object["averprice"]
        temp["blockName"] = object["blockinfo"]["blockname"]
        temp["buildArea"] = object["buildarea"]
        temp["buildYear"] = object["buildyear"]
        temp["district"] = object["district"]
        temp["fitment"] = object["fitment"]
        temp["floor"] = object["floor"]
        temp["forward"] = object["forward"]
        temp["hall"] = object["hall"]
        temp["houseId"] = object["id"]
        temp["mright"] = object["mright"]
        temp["price"] = object["price"]
        temp["room"] = object["room"]
        temp["streetName"] = object["streetname"]
        temp["toilet"] = object["toilet"]
        temp["totalFloor"] = object["totalfloor"]
        temp_list.append(temp)
        resultMap['pois'] = temp_list
        logging.debug(json.dumps(resultMap, ensure_ascii=False))
    return json.dumps(resultMap, ensure_ascii=False)


def get_history(phone):
    deviceid = relation(phone)
    filepath = approot.get_dataset("select_DEVICE_ID_CONTEXT_ID__from_DWB_DA.csv")
    data = pd.read_csv(filepath)
    data.columns = ['deviceId', 'contentId']
    data = data[data['deviceId'] == deviceid]
    contentIds = get_contentIds(data)
    secondHouseData = secondHouseRequest2(contentIds)
    data = json.loads(secondHouseData)
    if len(data['pois']) == 0:
        return "no history"
    else:
        return secondHouseData


def getBlockCoord(blockName):
    filepath = approot.get_dataset("coord_blocks.json")
    file = open(filepath, 'r')
    block_coord_json = json.load(file)
    if blockName in block_coord_json:
        return block_coord_json[blockName]
    else:
        return None


if __name__ == '__main__':
    # datas = startup("18055500055")
    # if type(datas) == str:
    #     print(datas)
    # else:
    #     secondHouseRequestJson(datas)

    print(get_history("18055500055"))

    # print(getBlockCoord("天润城第十四街区"))
