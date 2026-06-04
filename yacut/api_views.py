from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_short, get_short_id


@app.route('/api/<int:id>/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if 'original_link' not in data:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    if custom_id == 'files':
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(URLMap)
    db.session.commit()
    return jsonify({'url_map': url_map.to_dict()}),201


@app.route('/api/<int:id>/short_id/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден')
    return jsonify({
        'url': url_map.original
    }), 200





