from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm, FileForm
from .models import URLMap
from .utils import get_unique_short_id
from .yandex_disk import async_upload_files_to_yandex_disk


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data
        short_id = custom_id or get_unique_short_id()
        if short_id == 'files' or URLMap.query.filter_by(
                short=short_id).first():
            flash('Такой вариант короткой ссылки уже существует!')
            return render_template('urls.html', form=form)
        url_map = URLMap(
            original=original,
            short=short_id,
        )
        db.session.add(url_map)
        db.session.commit()
        short_url = url_for(
            'redirect_view',
            short_id=short_id,
            _external=True,
        )
        return render_template(
            'urls.html',
            form=form,
            short_url=short_url,
        )
    return render_template('urls.html', form=form)


@app.route('/<short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileForm()
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
                    'redirect_view',
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
