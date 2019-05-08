import os
from collections import OrderedDict

from requests import Session


UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY', '')


class UnsplashApi:
    api_url = 'https://api.unsplash.com/'
    _headers = {
        'Accept-Version': '1',
    }
    _session = Session()

    @classmethod
    def get(cls, *args, **kwargs):
        params = kwargs.pop('params', {})
        params = OrderedDict(
            client_id=UNSPLASH_ACCESS_KEY,
            **params
        )
        kwargs['params'] = params
        print(params)
        return cls._session.get(cls.api_url, **kwargs)

    def post(self, *args, **kwargs):
        return super().post(
            "{}?client_id={}".format(
                self.api_url,
                UNSPLASH_ACCESS_KEY
            ), *args, **kwargs
        )

    def put(self, *args, **kwargs):
        return super().put(self.api_url, *args, **kwargs)

    def head(self, *args, **kwargs):
        return super().head(self.api_url, *args, **kwargs)


class UnsplashPhotoFilter:
    order_by = 'popular' # [latest, oldest, popular]
    page = 1
    per_page = 10


class UnsplashPhotos(UnsplashApi):
    api_url = "{}photos".format(UnsplashApi.api_url)

    @classmethod
    def get(cls, query_filter=None, *args, **kwargs):
        if query_filter:
            params = kwargs.pop('params', {})
            params.update(
                order_by=query_filter.order_by,
                page=query_filter.page,
                per_page=query_filter.per_page,
            )
            kwargs['params'] = params
        return super(cls, cls).get(**kwargs)


class UnsplashPhoto(UnsplashApi):
    api_url = '{}/'.format(UnsplashPhotos.api_url)

    @classmethod
    def get(cls, photo_id=None, random=False, **kwargs):
        assert ((not photo_id) or (not random)), \
            'cannot ask for random image and pass an id'

        cls.api_url = "{}{}".format(
            cls.api_url,
            photo_id or random and 'random'
        )
        return super(cls, cls).get(**kwargs)
