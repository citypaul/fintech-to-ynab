from flask import Blueprint

import settings
import ynab_client
from main import create_transaction_from_starling, create_transaction_from_bankin, create_transaction_from_monzo

main_blueprints = Blueprint('main',__name__)

from functools import wraps

from flask import request, jsonify
from werkzeug.utils import redirect

@main_blueprints.route('/')
def route_index():
    return redirect("https://github.com/scottrobertson/fintech-to-ynab", code=302)

@main_blueprints.route('/ping')
def route_ping():
    return 'pong'

def secret_required(func):
    '''
    :param func: The view function to decorate.
    :type func: function
    '''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if settings.url_secret is not None and settings.url_secret != request.args.get('secret'):
            return jsonify({'error': 'Invalid secret'}), 403
        return func(*args, **kwargs)
    return decorated_view


def common_view(create_transaction_func):
    data = request.get_json()
    settings.log.debug(data)
    ynab_client.init()

    body, code = create_transaction_func(data, settings, 0)
    return jsonify(body), code


@secret_required
@app.route('/starling', methods=['POST'])
def route_starling():
    return common_view(create_transaction_from_starling)


@secret_required
@app.route('/bankin', methods=['POST'])
def route_bankin():
    return common_view(create_transaction_from_bankin)


@secret_required
@app.route('/monzo', methods=['POST'])
def route_monzo():
    return common_view(create_transaction_from_monzo)