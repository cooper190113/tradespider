import csv
import os
import datetime
import sys

from search.config import LOGGER


def read_file(filename, default=''):
    """
    Get data from a file
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
    user_agents_file = os.path.join(os.path.join(root_folder, 'data'), filename)
    try:
        with open(user_agents_file) as fp:
            data = [_.strip() for _ in fp.readlines()]
    except Exception as ex:
        LOGGER.info("Get data from {} is error:{}", filename, ex)
        data = [default]
    return data


def save(desc, data):
    """
    save csv
    :param data: iterator []
    :param desc: filename
    :return:
    """
    with open(desc + "_" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "_data.csv",
              'w', newline='', encoding='utf-8-sig') as f:
        for result in data:
            f_csv = csv.writer(f)
            f_csv.writerow(result)
