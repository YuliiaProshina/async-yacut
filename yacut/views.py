import random
import string

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .constants import SHORT_LINK_LENGTH
from .forms import URLMapForm, FileForm
from .models import URLMap


def get_unique_short_id(SHORT_LINK_LENGTH):
    VALID_CHARS = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choice(VALID_CHARS) for _ in range(SHORT_LINK_LENGTH))
        if URLMap.query.filter_by(unique_short_id=short_id).first() is None:
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        custom_id  = form.short_id.data
        short_id = custom_id or get_unique_short_id()
        if short_id == 'files' or URLMap.query.filter_by(short=short_id).first():
            flash('Такой вариант короткой ссылки уже существует!')
            return render_template('index.html', form=form)
        url_map = URLMap(
            original=original,
            short=short_id,
        )
        db.session.add(url_map)
        db.session.commit()

    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.get_or_404(short_id)
    return redirect(url_map.original)


@app.route('/files')
async def files_view():
    form = FileUploadForm()
    uploaded_files = []

    if form.validate_on_submit():
        files = form.files.data

        urls = await async_upload_files_to_yandex_disk(files)

        for file_storage, download_link in zip(files, urls):
            short_id = get_unique_short_id()

            url_map = URLMap(
                original=download_link,
                short=short_id,
            )

            db.session.add(url_map)

            uploaded_files.append({
                'filename': file_storage.filename,
                'short_url': url_for(
                    'main.redirect_view',
                    short_id=short_id,
                    _external=True,
                ),
            })

        db.session.commit()

    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files,
    )
