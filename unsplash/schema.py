import graphene


from bunch import bunchify

from unsplash.api import (
    UnsplashPhotos,
    UnsplashPhoto,
    UnsplashPhotoFilter,
)


keys = [
    'id', 'created_at', 'updated_at', 'width',
    'height', 'color', 'description',
    'alt_description', 'urls', 'links',
    'categories', 'sponsored', 'sponsored_by',
    'sponsored_impressions_id', 'likes',
    'liked_by_user', 'current_user_collections',
    'user', 'exif', 'location', 'views', 'downloads'
]


class LinkObjectType(graphene.ObjectType):
    self = graphene.String(
        description='rest api link for this photo'
    )
    html = graphene.String(
        description='html page link for this photo'
    )
    download = graphene.String(
        description='download link for this photo'
    )
    download_location = graphene.String(
        description='host for download link'
    )


class UrlObjectType(graphene.ObjectType):
    raw = graphene.String(
        description='raw image url'
    )
    full = graphene.String(
        description='full image url'
    )
    regular = graphene.String(
        description='regular image url'
    )
    small = graphene.String(
        description='small image url'
    )
    thumb = graphene.String(
        description='thumbnail image url'
    )


class PhotoObjectType(graphene.ObjectType):
    id = graphene.ID(
        description='unsplash photo id'
    )
    created_at = graphene.DateTime(
        description='iso datetime string of when photo was created'
    )
    updated_at = graphene.DateTime(
        description='iso datetime string of when photo was modified'
    )
    width = graphene.Int(
        description='width of the requested image'
    )
    height = graphene.Int(
        description='height of the requested image'
    )
    color = graphene.String(
        description='main color of the requested image'
    )
    description = graphene.String(
        description='description of the requested image'
    )
    alt_description = graphene.String(
        description='alternate description of the requested image'
    )
    urls = graphene.Field(
        UrlObjectType,
        description='related urls for requested image'
    )
    links = graphene.Field(
        LinkObjectType,
        description='related links for requested image'
    )
    sponsored = graphene.Boolean(
        description='is the image sponsored?'
    )
    views = graphene.Int(
        description='number of views for requested image'
    )
    downloads = graphene.Int(
        description='number of downloads for requested image'
    )
    liked_by_user = graphene.Boolean(
        description='if the current use has liked this image'
    )
    likes = graphene.Int(
        description='how many like the image has'
    )



class OrderByEnum(graphene.Enum):
    class Meta:
        description = 'how to order photo result list'

    LATEST = 'latest'
    OLDEST = 'oldest'
    POPLAR = 'popular'


class PhotoQueryFilterInputType(graphene.InputObjectType):
    order_by = OrderByEnum()
    page = graphene.Int(
        default_value=1,
        description='page number for returned results'
    )
    per_page = graphene.Int(
        default_value=10,
        description='number of results per page'
    )


class PhotoQuery(graphene.ObjectType):
    get_photos = graphene.List(
        PhotoObjectType,
        query_filter=graphene.Argument(
            PhotoQueryFilterInputType
        ),
        description='get a list of photos'
    )
    get_photo = graphene.Field(
        PhotoObjectType,
        id=graphene.ID(required=True),
        description='get a single photo by id'
    )
    get_random_photo = graphene.Field(
        PhotoObjectType,
        description='get a random photo'
    )

    def resolve_get_photos(self, info, query_filter=None, **kwargs):
        photos = [
            photo
            for photo in UnsplashPhotos.get(
                query_filter=query_filter
            ).json()
        ]
        for photo in photos:
            photo.pop('categories','')
            photo.pop('sponsored_by','')
            photo.pop('sponsored_impressions_id','')
            photo.pop('likes','')
            photo.pop('liked_by_user','')
            photo.pop('current_user_collections','')
            photo.pop('user','')
            photo.pop('exif','')
            photo.pop('location','')
            photo.pop('sponsorship', '')
        return [
            PhotoObjectType(**photo) for photo in photos
        ]


    def resolve_get_photo(self, info, id=None, **kwargs):
        return bunchify(UnsplashPhoto.get(photo_id=id).json())

    def resolve_get_random_photo(self, info, **kwargs):
        return bunchify(UnsplashPhoto.get(random=True).json())




class Query(PhotoQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=Query,
    auto_camelcase=False,
)