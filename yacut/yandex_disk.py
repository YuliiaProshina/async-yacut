import asyncio

import aiohttp

from . import app


AUTH_HEADERS = {
    'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'
}

UPLOAD_LINK = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
DOWNLOAD_LINK = 'https://cloud-api.yandex.net/v1/disk/resources/download'


async def async_upload_files_to_yandex_disk(files):
    if files is not None:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for file in files:
                tasks.append(
                    asyncio.ensure_future(
                        upload_file_and_get_url(session, file)
                    )
                )
            urls = await asyncio.gather(*tasks)
        return urls


async def upload_file_and_get_url(session, file):
    file_path = f'app:/{file.filename}'
    upload_params = {
        'path': file_path,
        'overwrite': 'true',
    }
    async with session.get(
        UPLOAD_LINK,
        headers=AUTH_HEADERS,
        params=upload_params,
    ) as response:
        if response.status != 200:
            print('YANDEX STATUS:', response.status)
            print('YANDEX RESPONSE:', await response.text())
        response.raise_for_status()
        data = await response.json()
        upload_url = data['href']
    file.stream.seek(0)
    file_data = file.read()
    async with session.put(
        upload_url,
        data=file_data,
    ) as response:
        response.raise_for_status()
    async with session.get(
        DOWNLOAD_LINK,
        headers=AUTH_HEADERS,
        params={'path': file_path},
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return data['href']