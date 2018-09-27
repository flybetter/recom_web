from flask import Blueprint, render_template
import redis
import pandas as pd
import json

new_house = Blueprint("newhouse", __name__, url_prefix="/newhouse")

r = redis.Redis(host='192.168.10.221', port=6379, db=1)

NEWHOUSELOG_PREFIX = "NHLOG^"
PHONEDEVICE_PREFIX = "PD^"


# @new_house.route("/<string:phone>/<int:num>")
# def newhouse(deviceid, num):
#     datas = r.lrange(NEWHOUSELOG_PREFIX + deviceid, 0, num)
#     result = list()
#     for data in datas:
#         result.extend(json.loads(data.decode('utf-8')))
#     return render_template("map/newhouse.html", newhouses=json.dumps(result, ensure_ascii=False), userId=deviceid,
#                            num=num)


@new_house.route("/<string:phone>/<int:num>")
def newhouse(phone, num):
    deviceids = r.smembers(PHONEDEVICE_PREFIX + phone)
    result = list()
    for deviceid in deviceids:
        result = list()
        datas = r.lrange(NEWHOUSELOG_PREFIX + deviceid.decode('utf-8'), 0, num)
        for data in datas:
            result.extend(json.loads(data.decode('utf-8')))
    return render_template("map/newhouse.html", newhouses=json.dumps(result, ensure_ascii=False), userId=deviceid,
                           num=num)


if __name__ == '__main__':
    phone = '13851729904'
    deviceids = r.smembers(PHONEDEVICE_PREFIX + phone)
    for deviceid in deviceids:
        print(deviceid.decode('utf-8'))
        num = 30
        result = list()
        datas = r.lrange(NEWHOUSELOG_PREFIX + deviceid.decode('utf-8'), 0, num)
        for data in datas:
            print(data.decode('utf-8'))
            result.extend(json.loads(data.decode('utf-8')))

        print(json.dumps(result, ensure_ascii=False))
