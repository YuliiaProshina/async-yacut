from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class URLMapForm(FlaskForm):
    original_link = URLField('Длинная ссылка',
                             validators=[DataRequired(
                                 message='Обязательное поле'),
                                 Length(1, 128)])
    custom_id = StringField('Ваш вариант короткой ссылки',
                            validators=[Optional(), Length(1, 16),
                                        Regexp(r'^[A-Za-z0-9]*$',
                                               message='Допустимы '
                                                       'только латинские '
                                                       'буквы и цифры')])
    submit = SubmitField('Создать')


class FileForm(FlaskForm):
    files = MultipleFileField(validators=[DataRequired(
        message='Выберите хотя бы один файл')])
    submit = SubmitField('Загрузить')
