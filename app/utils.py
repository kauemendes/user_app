#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~
    Utility methods.
    I'm including this file in the skeleton because it contains methods I've
    found useful.

    The goal is to keep this file as lean as possible.

    :author: Jeff Kereakoglow
    :date: 2014-11-14
    :copyright: (c) 2014 by Alexis Digital
    :license: MIT, see LICENSE for more details
"""
import argparse
import datetime
import json
import string
from decimal import Decimal

import hashlib
import os
import psutil
import random
from boto.s3.connection import S3Connection
from dateutil.relativedelta import relativedelta
from flask import request, make_response, jsonify, abort
from pip._vendor.requests.packages.urllib3.connectionpool import xrange
from app.helper_kit.string_kit import StringKit


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


def get_error_descriptions(e):
    """
        GEN-001	Campo obrigatório não informado.
        GEN-002	Campo obrigatório informado vazio.
        GEN-003	Campo obrigatório do tipo Array deve conter pelo menos 1 item.
        GEN-004	Campo excedeu a quantidade máxima de caracteres.
        TYP-001	Tipo esperado STRING.
        TYP-002	Tipo esperado INTEGER.
        TYP-003	Data mal formatada: Esperado YYYY-MM-DD.
        TYP-004	Data-hora mal formatada: Esperado YYYY-MM-DD hh:mm:ss.
        TYP-005	Email inválido.
        TYP-006	CPF inválido. Informe apenas os números sem pontuação.
        TYP-007	Número de telefone inválido. Informe apenas os números sem pontuação.
        TYP-008	CRM inválido. Informe no formato 0000-XX, onde XX refere-se à sigla do estado.
        TYP-009	CRM inválido. A sigla informada não é válida.
        TYP-010	Formato de URL inválido
        TYP-011	Gênero informado inválido. Utilize 0 : Não definido; 1 : Masculino ou 2 : Feminino
        TYP-012	A sigla do estado brasileiro é inválida. Utilize um valor oficialmente aceito.
        ITC-001	Valor informado inválido. Utilize 0: Aguardando, 1: Não aprovado ou 2: Aprovado
        ITC-002	Valor do amount deve ser maior do que 0 (zero)
        MDT-001	Hospital não encontrado.
        MDT-002	OwnId não informado
        MDT-003	OwnId já existe
        MDT-004	Registro não encontrado
    """
    error_msgs_code = {
        "GEN-001": "Campo obrigatório não informado.",
        "GEN-002": "Campo obrigatório informado vazio.",
        "GEN-003": "Campo obrigatório do tipo Array deve conter pelo menos 1 item.",
        "GEN-004": "Campo excedeu a quantidade máxima de caracteres.",
        "GEN-005": "Campo com caracteres especiais ou espaços.",
        "GEN-006": "Campo inciando com caracteres especiais ou espaços.",
        "GEN-007": "Não foi possível parsear o arquivo.",
        "GEN-008": "Médico cadastrado sem e-mail.",
        "TYP-001": "Tipo esperado STRING.",
        "TYP-002": "Tipo esperado INTEGER.",
        "TYP-003": "Data mal formatada: Esperado YYYY-MM-DD.",
        "TYP-004": "Data-hora mal formatada: Esperado YYYY-MM-DD hh:mm:ss.",
        "TYP-005": "Email inválido.",
        "TYP-006": "CPF inválido. Informe apenas os números sem pontuação.",
        "TYP-007": "Número de telefone inválido. Informe apenas os números sem pontuação.",
        "TYP-008": "CRM inválido. Informe no formato 00000-XX, onde XX refere-se à sigla do estado.",
        "TYP-009": "CRM inválido. A sigla informada não é válida.",
        "TYP-010": "Formato de URL inválido",
        "TYP-011": "Gênero informado inválido. Utilize 0 : Não definido; 1 : Masculino ou 2 : Feminino",
        "TYP-012": "A sigla do estado brasileiro é inválida. Utilize um valor oficialmente aceito.",
        "ITC-001": "Valor informado inválido. Utilize 0: Aguardando, 1: Não aprovado ou 2: Aprovado",
        "ITC-002": "Valor do amount deve ser maior do que 0 (zero)",
        "MDT-001": "Hospital não encontrado.",
        "MDT-002": "OwnId não informado",
        "MDT-003": "OwnId já existe",
        "MDT-004": "Registro não encontrado",
        "TYP-013": "O campo CEP (zipcode) deve conter 8 digitos",
        "TYP-014": "Formato de arquivo não permitido"
    }
    if len(e) > 0:
        _erros_code = e.split(",")
        _errors_msg = ""
        for _er_cd in _erros_code:
            _errors_msg += ", {0}".format(error_msgs_code[_er_cd]) if _errors_msg is not "" else error_msgs_code[_er_cd]
    else:
        _errors_msg = e

    return _errors_msg


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


def fix_answers_from_wrong_options():
    print("+--- Preparing to update questions with answers ----+")
    from app import db
    from app.models.question import QuestionAnswer, QuestionOption
    question_answers = QuestionAnswer.query.filter(QuestionAnswer.answer_int is not None).all()

    print("+=======================================---------------+")
    print("| Amount of questions_answers to correct [{0}]  |".format(len(question_answers)))
    print("+=======================================---------------+")
    for ans in question_answers:
        question_opts = QuestionOption.query.filter_by(question_id=ans.question_id).all()
        try:
            print("+=======================================---------------+")
            print("| Trying to find correct answer in options [{0}]  |".format(len(question_opts)))
            print("+=======================================---------------+")
            question_opt = question_opts[ans.answer_int]
        except IndexError as ie:
            print("| Nothing to sync |")
            print("+=======================================---------------+")
            continue

        if ans.answer_int is question_opt.id:
            print("+=======================================---------------+")
            print("+- Already fixed -+")
            print("+=======================================---------------+")
            continue

        print("+=======================================---------------+")
        print("+- Fixing old ({0}) to new ({1}) -+".format(ans.answer_int, question_opt.id))
        print("+=======================================---------------+")
        ans.answer_int = question_opt.id
        db.session.commit()


def migrate_fields_redis_to_db():
    print("+--- Migrations Start ----+")
    import datetime
    from app import db
    from app.models.surgery import Surgery
    from app.hospital_models.surgery import SurgeryRedis

    _redis_surgeries = SurgeryRedis.query.all()

    for _redis_surgery in _redis_surgeries:
        print("+=======================================---------------+")
        print("+--- SurgeryRedis----+")
        print("+=======================================---------------+")
        print("+--- {0}----+".format(_redis_surgery.reference_id))
        print("+=======================================---------------+")
        _surgery_db = Surgery.query.filter_by(reference_id=_redis_surgery.reference_id).first()
        print("+--- {0}----+".format(_surgery_db.reference_id))
        print("+=======================================---------------+")
        if _surgery_db:
            print("+----------------- Entrou ------------------+")
            if _surgery_db.surgery_code is None:
                print("+----------------- updateSuperSearch------------------+")
                _surgery_db.surgery_code = _redis_surgery.surgery_code

            if _surgery_db.doctor_searchable is None:
                print("+----------------- updateSuperSearch------------------+")
                _surgery_db.doctor_searchable = _redis_surgery.doctor_searchable

            if _surgery_db.patient_searchable is None:
                print("+----------------- patient_searchable ------------------+")
                _surgery_db.patient_searchable = _redis_surgery.patient_searchable

            if _surgery_db.hospital_room_searchable is None:
                print("+----------------- hospital_room_searchable ------------------+")
                _surgery_db.hospital_room_searchable = _redis_surgery.hospital_room_searchable

            if _surgery_db.health_insurance_search is None:
                print("+----------------- health_insurance_search ------------------+")
                _surgery_db.health_insurance_search = _redis_surgery.health_insurance_search

            if _surgery_db.super_search is None:
                print("+----------------- super_search ------------------+")
                _surgery_db.super_search = _redis_surgery.super_search

            # convertdates
            date_created_at = datetime.datetime.fromtimestamp(_redis_surgery.date_created_at)
            date_start = datetime.datetime.fromtimestamp(_redis_surgery.date_start)
            date_end = datetime.datetime.fromtimestamp(_redis_surgery.date_end)

            if _surgery_db.date_created_at is None:
                print("+----------------- date_created_at ------------------+")
                _surgery_db.date_created_at = date_created_at

            if _surgery_db.date_start is None:
                print("+----------------- date_start ------------------+")
                if date_start.year == 1969:
                    _surgery_db.date_start = None
                else:
                    _surgery_db.date_start = date_start

            if _surgery_db.date_end is None:
                print("+----------------- date_end ------------------+")
                if date_end.year == 1969:
                    _surgery_db.date_end = None
                else:
                    _surgery_db.date_end = date_end

    db.session.commit()
    print("+-------------- DONE UPDATING ---------------+")


def clear_old_tokens_without_update():
    from app import db
    from app.services_legacy.authorization_server import Token
    import datetime
    date_now = datetime.datetime.utcnow()
    date_now = date_now - relativedelta(days=30)
    Token.query.filter(Token.expires <= date_now, Token.scope == "hospital user").delete()
    db.session.commit()


def process_type_normalize(desc):
    from app.models.view import ProcessType
    desc = StringKit.normalize_string(desc).upper()
    try:
        return ProcessType(desc)
    except Exception as e:
        return None


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


def verification_is_pickup_is_running():
    count = 0
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
            if "python" in p.name():
                if len(p.cmdline()) > 1:
                    for cmd in p.cmdline():
                        if "robot_sugery_pickup" in cmd:
                            print("PICKUP IS RUNNING - WAIT...")
                            count += 1
        except Exception as e:
            pass
    if count >= 2:
        return True
    return False


def verification_is_process_running():
    count = 0
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
            if "python" in p.name():
                if len(p.cmdline()) > 1:
                    for cmd in p.cmdline():
                        if "process_surgeries" in cmd:
                            print("Process Surgeries IS RUNNING - WAIT...")
                            count += 1
        except Exception as e:
            pass
    if count >= 2:
        return True
    return False

