from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id, is_valid_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    custom_id = data.get('custom_id')
    if not custom_id:
        short_id = get_unique_short_id()
    elif not is_valid_short_id(custom_id):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки'
        )
    elif (custom_id == 'files' or
            URLMap.query.filter_by(short=custom_id).first() is not None):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    else:
        short_id = custom_id
    url_map = URLMap(
        original=data['url'],
        short=short_id,
    )
    db.session.add(url_map)
    db.session.commit()
    return jsonify({
        'url': url_map.original,
        'short_link': url_for(
            'redirect_view',
            short_id=url_map.short,
            _external=True,
        ),
    }), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND,)

    return jsonify({
        'url': url_map.original,
    }), HTTPStatus.OK
