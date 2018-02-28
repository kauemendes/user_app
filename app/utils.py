#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import datetime
import json
from decimal import Decimal

import hashlib
import random
from flask import request, make_response, jsonify, abort
from pip._vendor.requests.packages.urllib3.connectionpool import xrange


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def prepare_json_response(success, message, data, codes=None, messages=None, total_pages=None, total_itens=None, current_page=None):
    if success:
        response = {"meta":
                        {"success": success,
                         "request": request.url,
                         "total_pages": total_pages,
                         "total_itens": total_itens,
                         "current_page": current_page},
                    "data": data
                    }
        if data:
            response["meta"]["data_count"] = len(data)
        if message:
            response["meta"]["message"] = message
    else:
        response = {
                    "meta":
                    {
                        "success": success,
                        "request": request.url,
                        "total_pages": total_pages,
                        "total_itens": total_itens,
                        "current_page": current_page
                    },
                    "errors":
                    {
                        "message": message,
                        "code": codes,
                        "request": request.url,
                        "path": request.url,
                        "description": messages
                    }
                }

    return response


def generate_random_phone():
    n = '000000000000'
    while '11' in n[3:6] or n[3:6] == '000' or n[6] == n[7] == n[8] == n[9] == n[10] == n[11]:
        n = str(random.randint(10 ** 9, 10 ** 10 - 1))
    return '(' + n[:2] + ')' + ' ' + n[:5] + '-' + n[6:]


def cpf_funcional():
    n = [random.randrange(10) for i in xrange(9)]

    # calcula digito 1 e acrescenta ao numero
    s = sum(x * y for x, y in zip(n, range(10, 1, -1)))
    d1 = 11 - s % 11
    if d1 >= 10:
        d1 = 0
    n.append(d1)

    # calcula digito 2 e acrescenta ao numero
    s = sum(x * y for x, y in zip(n, range(11, 1, -1)))
    d2 = 11 - s % 11
    if d2 >= 10:
        d2 = 0
    n.append(d2)

    return "%d%d%d%d%d%d%d%d%d%d%d" % tuple(n)


def error_response(e):
    if hasattr(e, "name"):
        if e.name == "Not Found":
            return abort(404)

    messages = get_error_descriptions(e)

    if "args" in e:
        codes = e.args[0]
    else:
        codes = e

    if not isinstance(messages, str) and "name" in messages:
        messages = messages.name
    elif not isinstance(messages, str):
        messages = ""

    return make_response(
        jsonify(prepare_json_response(
            message="JSON not found",
            success=False,
            data={},
            codes=codes,
            messages=messages
        )), 400)


def valid_datetime_start(s: str):
    if not s:
        return None

    try:
        return datetime.datetime.strptime(s.rstrip() + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        msg = "Not a valid date start: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def valid_datetime_end(s: str):
    if not s:
        return None
    try:
        return datetime.datetime.strptime(s.rstrip() + " 23:59:59", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        msg = "Not a valid date end: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def hash_sha1(s):
    hash_client_id = hashlib.sha1()
    hash_client_id.update(s.encode())
    return hash_client_id.hexdigest()
