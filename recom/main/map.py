from flask import render_template, Blueprint

from urllib import request
import json

bp = Blueprint('map', __name__, url_prefix='/map')

HISTORY_URL = 'http://tuijianapiv2.house365.com/analysis/getData?cityKey=nj&dataType=accesslog&pageNum=1&pageSize=20&' \
              'userId='


@bp.route('/')
def hello_world():
    return render_template('map/map.html')


@bp.route('/<string:phone>/history', methods=('GET', 'POST'))
def history(phone):
    response = request.urlopen(HISTORY_URL + phone)
    return str(response.read().decode('utf-8'))


