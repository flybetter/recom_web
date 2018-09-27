from flask import render_template, Blueprint

from urllib import request
import json
from recom.main.recom_glorithm import startup, secondHouseRequestJson, get_history, get_associate_community
import logging

logging.basicConfig(level=logging.DEBUG)

bp = Blueprint('map', __name__, url_prefix='/map')

HISTORY_URL = 'http://tuijianapiv2.house365.com/analysis/getData?cityKey=nj&dataType=accesslog&pageNum=1&pageSize=20&' \
              'userId='


@bp.route('/')
def hello_world():
    return render_template('map/map.html')


@bp.route('/<string:phone>/history', methods=('GET', 'POST'))
def history(phone):
    # response = request.urlopen(HISTORY_URL + phone)
    return get_history(phone)


@bp.route('/<string:phone>/recom', methods=('GET', 'POST'))
def recom(phone):
    datas = startup(phone)
    if type(datas) != str:
        datas = secondHouseRequestJson(datas)
    return datas


@bp.route('/<string:phone>/associated_community', methods=('GET', 'POST'))
def associated_community(phone):
    return get_associate_community(phone)
