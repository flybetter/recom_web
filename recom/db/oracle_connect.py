# coding=utf-8
import cx_Oracle
import os
import logging

logging.basicConfig(level=logging.DEBUG)

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

HOST = 'app/app@202.102.83.165/app'

ORACL_SQL = "select ID from dwb_ras_sell_nj_all sample(50)" \
            " where BLOCKSHOWNAME in %s and esta =1 and PRICE between %d and %d and rownum<10"

ORACL_SQL_2 = "select ID from dwb_ras_sell_nj_all sample(50)" \
              " where BLOCKSHOWNAME in %s and esta =1 and rownum<10"


def oracle_connection(host=HOST):
    connection = cx_Oracle.connect(host)
    cursor = connection.cursor()
    return connection, cursor


def get_data(blocknames, lowPrice, highPrice):
    blocknames = tuple(blocknames)
    blocknames = "{}".format(blocknames)
    sql = ORACL_SQL % (blocknames, lowPrice, highPrice)
    logging.debug(sql)
    connection, cursor = oracle_connection()
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data) == 0:
        sql = ORACL_SQL_2 % blocknames
        cursor.execute(sql)
        logging.debug(sql)
        data = cursor.fetchall()
    oracle_close(connection, cursor)
    for object in data:
        logging.info(object)
    return data


def oracle_close(connection, cursor):
    cursor.close()
    connection.close()


if __name__ == '__main__':
    blocknames = ["苏宁名都汇", "江南青年城"]
    get_data(blocknames, 200, 300)
