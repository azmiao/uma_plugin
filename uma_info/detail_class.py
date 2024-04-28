from datetime import datetime
from typing import Any, List, TypeVar, Type, cast, Callable, Optional

import dateutil.parser

T = TypeVar('T')


def from_str(x: Any) -> str:
    if not x:
        return ''
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> Optional[datetime]:
    if not x:
        return None
    return dateutil.parser.parse(x)


def from_int(x: Any) -> int:
    if not x:
        return 0
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    if not x:
        return x
    assert isinstance(x, bool)
    return x


def format_datetime(x: Optional[datetime]) -> Optional[str]:
    if not x:
        return None
    return x.isoformat()


class Affiliation:
    id: str
    created_at: datetime
    updated_at: datetime
    published_at: datetime
    revised_at: datetime
    title: str

    def __init__(self, id: str, created_at: datetime, updated_at: datetime, published_at: datetime,
                 revised_at: datetime, title: str) -> None:
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.published_at = published_at
        self.revised_at = revised_at
        self.title = title

    @staticmethod
    def from_dict(obj: Any) -> 'Affiliation':
        if not obj or not isinstance(obj, dict):
            return Affiliation(**{key: None for key in Affiliation.__annotations__.keys()})
        id = from_str(obj.get('id'))
        created_at = from_datetime(obj.get('createdAt', None))
        updated_at = from_datetime(obj.get('updatedAt', None))
        published_at = from_datetime(obj.get('publishedAt', None))
        revised_at = from_datetime(obj.get('revisedAt', None))
        title = from_str(obj.get('title', ''))
        return Affiliation(id, created_at, updated_at, published_at, revised_at, title)

    def to_dict(self) -> dict:
        result: dict = {
            'id': from_str(self.id),
            'createdAt': format_datetime(self.created_at),
            'updatedAt': format_datetime(self.updated_at),
            'publishedAt': format_datetime(self.published_at),
            'revisedAt': format_datetime(self.revised_at),
            'title': from_str(self.title)
        }
        return result


class ListThumb:
    url: str
    height: int
    width: int

    def __init__(self, url: str, height: int, width: int) -> None:
        self.url = url
        self.height = height
        self.width = width

    @staticmethod
    def from_dict(obj: Any) -> 'ListThumb':
        if not obj or not isinstance(obj, dict):
            return ListThumb(**{key: None for key in ListThumb.__annotations__.keys()})
        url = from_str(obj.get('url', ''))
        height = from_int(obj.get('height', 0))
        width = from_int(obj.get('width', 0))
        return ListThumb(url, height, width)

    def to_dict(self) -> dict:
        result: dict = {
            'url': from_str(self.url),
            'height': from_int(self.height),
            'width': from_int(self.width)
        }
        return result


class Download:
    field_id: str
    icon: ListThumb
    header: ListThumb

    def __init__(self, field_id: str, icon: ListThumb, header: ListThumb) -> None:
        self.field_id = field_id
        self.icon = icon
        self.header = header

    @staticmethod
    def from_dict(obj: Any) -> 'Download':
        if not obj or not isinstance(obj, dict):
            return Download(**{key: None for key in Download.__annotations__.keys()})
        field_id = from_str(obj.get('fieldId', ''))
        icon = ListThumb.from_dict(obj.get('icon', {}))
        header = ListThumb.from_dict(obj.get('header', {}))
        return Download(field_id, icon, header)

    def to_dict(self) -> dict:
        result: dict = {
            'fieldId': from_str(self.field_id),
            'icon': to_class(ListThumb, self.icon),
            'header': to_class(ListThumb, self.header)
        }
        return result


class Visual:
    field_id: str
    name: Affiliation
    thumb: ListThumb
    image: ListThumb

    def __init__(self, field_id: str, name: Affiliation, thumb: ListThumb, image: ListThumb) -> None:
        self.field_id = field_id
        self.name = name
        self.thumb = thumb
        self.image = image

    @staticmethod
    def from_dict(obj: Any) -> 'Visual':
        if not obj or not isinstance(obj, dict):
            return Visual(**{key: None for key in Visual.__annotations__.keys()})
        field_id = from_str(obj.get('fieldId', ''))
        name = Affiliation.from_dict(obj.get('name', {}))
        thumb = ListThumb.from_dict(obj.get('thumb', {}))
        image = ListThumb.from_dict(obj.get('image', {}))
        return Visual(field_id, name, thumb, image)

    def to_dict(self) -> dict:
        result: dict = {
            'fieldId': from_str(self.field_id),
            'name': to_class(Affiliation, self.name),
            'thumb': to_class(ListThumb, self.thumb),
            'image': to_class(ListThumb, self.image)
        }
        return result


class Voice:
    url: str

    def __init__(self, url: str) -> None:
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'Voice':
        if not obj or not isinstance(obj, dict):
            return Voice(**{key: None for key in Voice.__annotations__.keys()})
        url = from_str(obj.get('url', ''))
        return Voice(url)

    def to_dict(self) -> dict:
        result: dict = {
            'url': from_str(self.url)
        }
        return result


class Adapt:
    grass: str
    mud: str
    short: str
    mile: str
    middle: str
    long: str
    run_away: str
    first: str
    center: str
    chase: str

    def __init__(self, grass: str, mud: str, short: str, mile: str, middle: str, long: str, run_away: str,
                 first: str, center: str, chase: str) -> None:
        self.grass = grass
        self.mud = mud
        self.short = short
        self.mile = mile
        self.middle = middle
        self.long = long
        self.run_away = run_away
        self.first = first
        self.center = center
        self.chase = chase

    @staticmethod
    def from_dict(obj: Any) -> 'Adapt':
        if not obj or not isinstance(obj, dict):
            return Adapt(**{key: None for key in Adapt.__annotations__.keys()})
        grass = from_str(obj.get('grass', ''))
        mud = from_str(obj.get('mud', ''))
        short = from_str(obj.get('short', ''))
        mile = from_str(obj.get('mile', ''))
        middle = from_str(obj.get('middle', ''))
        long = from_str(obj.get('long', ''))
        run_away = from_str(obj.get('run_away', ''))
        first = from_str(obj.get('first', ''))
        center = from_str(obj.get('center', ''))
        chase = from_str(obj.get('chase', ''))
        return Adapt(grass, mud, short, mile, middle, long, run_away, first, center, chase)

    def to_dict(self) -> dict:
        result: dict = {
            'grass': from_str(self.grass),
            'mud': from_str(self.mud),
            'short': from_str(self.short),
            'mile': from_str(self.mile),
            'middle': from_str(self.middle),
            'long': from_str(self.long),
            'run_away': from_str(self.run_away),
            'first': from_str(self.first),
            'center': from_str(self.center),
            'chase': from_str(self.chase)
        }
        return result


class Uma:
    id: str
    created_at: datetime
    updated_at: datetime
    published_at: datetime
    revised_at: datetime
    name: str
    en: str
    catch: str
    cv: str
    category: List[str]
    affiliation: Affiliation
    earring: List[str]
    color_main: str
    color_sub: str
    birthday: str
    height: str
    weight: str
    size: str
    detail: str
    movie_id: str
    is_top: bool
    is_music: bool
    list_thumb: ListThumb
    top_thumb: ListThumb
    visual: List[Visual]
    voice: Voice
    download: Download
    cn_name: str
    adapt: Adapt

    def __init__(self, id: str, created_at: datetime, updated_at: datetime, published_at: datetime,
                 revised_at: datetime, name: str, en: str, catch: str, cv: str, category: List[str],
                 affiliation: Affiliation, earring: List[str], color_main: str, color_sub: str, birthday: str,
                 height: str, weight: str, size: str, detail: str, movie_id: str, is_top: bool, is_music: bool,
                 list_thumb: ListThumb, top_thumb: ListThumb, visual: List[Visual], voice: Voice,
                 download: Download, cn_name: str, adapt: Adapt) -> None:
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.published_at = published_at
        self.revised_at = revised_at
        self.name = name
        self.en = en
        self.catch = catch
        self.cv = cv
        self.category = category
        self.affiliation = affiliation
        self.earring = earring
        self.color_main = color_main
        self.color_sub = color_sub
        self.birthday = birthday
        self.height = height
        self.weight = weight
        self.size = size
        self.detail = detail
        self.movie_id = movie_id
        self.is_top = is_top
        self.is_music = is_music
        self.list_thumb = list_thumb
        self.top_thumb = top_thumb
        self.visual = visual
        self.voice = voice
        self.download = download
        self.cn_name = cn_name
        self.adapt = adapt

    @staticmethod
    def from_dict(obj: Any) -> 'Uma':
        if not obj or not isinstance(obj, dict):
            return Uma(**{key: None for key in Uma.__annotations__.keys()})
        id = from_str(obj.get('id', ''))
        created_at = from_datetime(obj.get('createdAt', None))
        updated_at = from_datetime(obj.get('updatedAt', None))
        published_at = from_datetime(obj.get('publishedAt', None))
        revised_at = from_datetime(obj.get('revisedAt', None))
        name = from_str(obj.get('name', ''))
        en = from_str(obj.get('en', ''))
        catch = from_str(obj.get('catch', ''))
        cv = from_str(obj.get('cv', ''))
        category = from_list(from_str, obj.get('category', []))
        affiliation = Affiliation.from_dict(obj.get('affiliation', {}))
        earring = from_list(from_str, obj.get('earring', []))
        color_main = from_str(obj.get('color_main', ''))
        color_sub = from_str(obj.get('color_sub', ''))
        birthday = from_str(obj.get('birthday', ''))
        height = from_str(obj.get('height', ''))
        weight = from_str(obj.get('weight', ''))
        size = from_str(obj.get('size', ''))
        detail = from_str(obj.get('detail', ''))
        movie_id = from_str(obj.get('movie_id', ''))
        is_top = from_bool(obj.get('is_top', None))
        is_music = from_bool(obj.get('is_music', None))
        list_thumb = ListThumb.from_dict(obj.get('list_thumb', {}))
        top_thumb = ListThumb.from_dict(obj.get('top_thumb', {}))
        visual = from_list(Visual.from_dict, obj.get('visual', []))
        voice = Voice.from_dict(obj.get('voice', {}))
        download = Download.from_dict(obj.get('download', {}))
        cn_name = from_str(obj.get('cn_name', ''))
        adapt = Adapt.from_dict(obj.get('adapt', {}))
        return Uma(id, created_at, updated_at, published_at, revised_at, name, en, catch, cv, category, affiliation,
                   earring, color_main, color_sub, birthday, height, weight, size, detail, movie_id, is_top,
                   is_music, list_thumb, top_thumb, visual, voice, download, cn_name, adapt)

    def to_dict(self) -> dict:
        result: dict = {
            'id': from_str(self.id),
            'createdAt': format_datetime(self.created_at),
            'updatedAt': format_datetime(self.updated_at),
            'publishedAt': format_datetime(self.published_at),
            'revisedAt': format_datetime(self.revised_at),
            'name': from_str(self.name),
            'cn_name': from_str(self.cn_name),
            'en': from_str(self.en),
            'catch': from_str(self.catch),
            'cv': from_str(self.cv),
            'category': from_list(from_str, self.category),
            'affiliation': to_class(Affiliation, self.affiliation),
            'earring': from_list(from_str, self.earring),
            'color_main': from_str(self.color_main),
            'color_sub': from_str(self.color_sub),
            'birthday': from_str(self.birthday),
            'height': from_str(self.height),
            'weight': from_str(self.weight),
            'size': from_str(self.size),
            'detail': from_str(self.detail),
            'movie_id': from_str(self.movie_id),
            'is_top': from_bool(self.is_top),
            'is_music': from_bool(self.is_music),
            'list_thumb': to_class(ListThumb, self.list_thumb),
            'top_thumb': to_class(ListThumb, self.top_thumb),
            'visual': from_list(lambda x: to_class(Visual, x), self.visual),
            'voice': to_class(Voice, self.voice),
            'download': to_class(Download, self.download),
            'adapt': to_class(Adapt, self.adapt)
        }
        return result


def uma_from_dict(s: Any) -> Uma:
    return Uma.from_dict(s)


def uma_to_dict(x: Uma) -> dict:
    return to_class(Uma, x)
