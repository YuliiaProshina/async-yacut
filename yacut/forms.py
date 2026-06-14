from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import MAX_CUSTOM_ID_LENGTH, MAX_LINK_LENGTH, MIN_LENGTH


class URLMapForm(FlaskForm):
    original_link = URLField('Длинная ссылка',
                             validators=[DataRequired(
                                 message='Обязательное поле'),
                                 Length(MIN_LENGTH, MAX_LINK_LENGTH)])
    custom_id = StringField('Ваш вариант короткой ссылки',
                            validators=[Optional(),
                                        Length(MIN_LENGTH,
                                               MAX_CUSTOM_ID_LENGTH),
                                        Regexp(r'^[A-Za-z0-9]*$',
                                               message='Допустимы '
                                                       'только латинские '
                                                       'буквы и цифры')])
    submit = SubmitField('Создать')


class FileForm(FlaskForm):
    files = MultipleFileField(validators=[DataRequired(
        message='Выберите хотя бы один файл')])
    submit = SubmitField('Загрузить')
