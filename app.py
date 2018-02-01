# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import requests
import json
from pandas import DataFrame

from flask import Flask
from flask import request
from flask import make_response

from flask import Flask, render_template
import sys
import logging

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
# Flask app should start in global layout
app = Flask(__name__)

coins = {'Bitcoin': 'btc_jpy',
         'Ethereum': 'eth_jpy',
         'NEM': 'xem_jpy',
         'Bitcoin Cash': 'bch_jpy',
         'Ripple': 'xrp_jpy',
         'Monero': 'xmr_jpy',
         'Augur': 'rep_jpy',
         'Litecoin': 'ltc_jpy',
         'Lisk': 'lsk_jpy',
         'DASH': 'dash_jpy',
         'Factom': 'fct_jpy',
         'Ethereum Classic': 'etc_jpy',
         'Zcash': 'zec_jpy'
         }


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "check_Cryptocurrency":
        return {}
    base_url = 'https://coincheck.com/api/rate/'
    currency = get_currency(req)
    if currency is None:
        return {}
    url = base_url + currency
    data = requests.get(url).json()
    res = makeWebhookResult(currency, data)
    return res


@staticmethod
def get_currency(req):
    result = req.get("result")
    parameters = result.get("parameters")
    cryptocurrency = parameters.get("Cryptocurrency")
    if cryptocurrency is None:
        return None

    return coins[cryptocurrency]


def makeWebhookResult(currency, data):
    result = query.get('results')
    if result is None:
        return {}

    speech = "現在の" + currency + "の価格は" + data['rate'] + "です。"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-crypt"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
