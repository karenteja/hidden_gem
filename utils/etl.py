#!/usr/bin/env python

from os import path
import json
from typing import List, Optional, Dict, Set, Tuple, Any
from dataclasses import dataclass, field, replace
from dataclasses_json import dataclass_json
from random import sample, seed, randint

DEFAULT_PEOPLE_SOURCE = '../data/people.json'
DEFAULT_BAR_SOURCE = '../data/bars.json'
DEFAULT_NEW_PEOPLE_DEST = '../data/data_new.json'
DEFAULT_MAX_FAVORITES = 10
DEFAULT_MAX_SAVED_FOR_LATER = 20
DEFAULT_MAX_EXPLORED = 30


@dataclass(eq=True, frozen=True)
@dataclass_json
class USLocation:
    """A data class that represents location in the US."""
    address1: str = field(default="n/a")
    address2: Optional[str] = field(default=None)
    address3: Optional[str] = field(default=None)
    city: str = field(default="n/a")
    state: str = field(default="n/a")
    zip: str = field(default="n/a")


@dataclass(eq=True, frozen=True)
@dataclass_json
class Coordinates:
    """A data class that represents coordinates."""
    lat: float = field(default=0)
    lon: float = field(default=0)


@dataclass(eq=True, frozen=True)
@dataclass_json
class Bar:
    """A data class that represents a bar."""
    categories: Tuple[str] = field(default=())
    coordinates: Coordinates = field(default=Coordinates())
    image_url: str = field(default='n/a')
    is_closed: bool = field(default=True)
    location: USLocation = field(default=USLocation())
    name: str = field(default='n/a')  #
    id: str = field(default='n/a')
    phone: Optional[str] = field(default=None)
    price: Optional[str] = field(default=None)


@dataclass
@dataclass_json
class User:
    """A data class that represents a user."""
    id: int = field(default=0)
    name: str = field(default='n/a')
    username: str = field(default='n/a')
    email: str = field(default='n/a')
    password: str = field(default='n/a')
    img: str = field(default='n/a')
    bars: Dict = field(default_factory=lambda: {})


def check_data_present(user_source_path, bar_source_path):
    if path.exists(user_source_path) and path.exists(bar_source_path):
        return
    raise IOError('Data sources should exist.')


def parse_categories(business: Dict) -> Tuple[Any]:
    if business is None:
        raise ValueError("Business should be defined.")
    return tuple([x['alias'] for x in business['categories']])


def parse_coords(business: Dict) -> Coordinates:
    if business is None:
        raise ValueError("Business should be defined.")
    lat = business['coordinates']['latitude']
    lon = business['coordinates']['longitude']
    return Coordinates(lat, lon)


def parse_image_url(business: Dict) -> str:
    if business is None:
        raise ValueError("Business should be defined.")
    return business['image_url']


def parse_is_closed(business: Dict) -> bool:
    if business is None:
        raise ValueError("Business should be defined.")
    return business['is_closed']


def parse_location(business: Dict) -> USLocation:
    if business is None:
        raise ValueError("Business should be defined.")
    address1 = business['location']['address1']
    address2 = business['location']['address2']
    address3 = business['location']['address3']
    city = business['location']['city']
    state = business['location']['state']
    zip = business['location']['zip_code']
    return USLocation(address1, address2, address3, city, state, zip)


def parse_name(business: Dict) -> str:
    if business is None:
        raise ValueError("Business should be defined.")
    return business['name']


def parse_id(business: Dict) -> str:
    if business is None:
        raise ValueError("Business should be defined.")
    return business['id']


def parse_phone(business: Dict) -> Optional[str]:
    if business is None:
        raise ValueError("Business should be defined.")
    return business.get('phone', None)


def parse_price(business: Dict) -> Optional[str]:
    if business is None:
        raise ValueError("Business should be defined.")
    return business.get('price', None)


def load_bar_data(bar_source_path) -> List[Bar]:
    with open(bar_source_path, 'r') as f:
        json_object = json.load(f)
        bar_list = []
        for business_object in json_object:
            for business in business_object['businesses']:
                # print(business)
                price = parse_price(business)
                phone = parse_phone(business)
                id = parse_id(business)
                name = parse_name(business)
                location = parse_location(business)
                is_closed = parse_is_closed(business)
                image_url = parse_image_url(business)
                coords = parse_coords(business)
                categories = parse_categories(business)
                bar_list.append(Bar(categories, coords, image_url, is_closed, location, name, id, phone, price))
        return bar_list


def load_user_data(user_source_path) -> List[User]:
    with open(user_source_path, 'r') as f:
        users = json.load(f)
        user_list = []
        for user in users:
            id = user['id']
            name = user['name']
            username = user['username']
            email = user['email']
            password = user['password']
            img = user['img']
            user_list.append(User(id, name, username, email, password, img))
        return user_list


def create_user_bar_lists(bars: List[Bar], s: int) -> Dict:
    seed(s)
    selected = {}
    all_user_bars = set(sample(bars, DEFAULT_MAX_SAVED_FOR_LATER + DEFAULT_MAX_EXPLORED))
    selected['explored'] = sample(all_user_bars, randint(0, DEFAULT_MAX_EXPLORED))
    saved_for_later = all_user_bars - set(selected['explored'])
    selected['saved'] = sample(saved_for_later, min(randint(0, DEFAULT_MAX_SAVED_FOR_LATER), len(saved_for_later)))
    selected['favorite'] = sample(selected['explored'],
                                  min(randint(0, DEFAULT_MAX_FAVORITES), len(selected['explored'])))
    return selected


def set_user_bar_data(user: User, bars: Dict) -> User:
    return replace(user, bars=bars)


def augment_user_data(users: List[User], bars: List[Bar]) -> List[User]:
    return [set_user_bar_data(users[i], create_user_bar_lists(bars, i)) for i in range(0, len(users))]


def write_new_data(users: List[User], dest_name: str):
    with open(dest_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps([json.loads(user.to_json()) for user in users], indent=4, ensure_ascii=False))


def main():
    check_data_present(DEFAULT_PEOPLE_SOURCE, DEFAULT_BAR_SOURCE)
    users = augment_user_data(load_user_data(DEFAULT_PEOPLE_SOURCE), load_bar_data(DEFAULT_BAR_SOURCE))
    write_new_data(users, DEFAULT_NEW_PEOPLE_DEST)


if __name__ == '__main__':
    main()
