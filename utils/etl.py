#!/usr/bin/env python

from os import path
import json
from typing import List, Optional, Dict
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

DEFAULT_PEOPLE_SOURCE = '../data/people.json'
DEFAULT_BAR_SOURCE = '../data/bars.json'
DEFAULT_SEED = 0
DEFAULT_MAX_FAVORITES = 10
DEFAULT_MAX_SAVED_FOR_LATER = 20
DEFAULT_MAX_EXPLORED = 30


@dataclass
@dataclass_json
class USLocation:
    """A data class that represents location in the US."""
    address1: str = field(default="n/a")
    address2: Optional[str] = field(default=None)
    address3: Optional[str] = field(default=None)
    city: str = field(default="n/a")
    state: str = field(default="n/a")
    zip: str = field(default="n/a")


@dataclass
@dataclass_json
class Coordinates:
    """A data class that represents coordinates."""
    lat: float = field(default=0)
    lon: float = field(default=0)


@dataclass
@dataclass_json
class Bar:
    """A data class that represents a bar."""
    categories: List[str] = field(default_factory=list)
    coordinates: Coordinates = field(default=Coordinates())
    image_url: str = field(default='n/a')
    is_closed: bool = field(default=True)
    location: USLocation = field(default=USLocation())
    name: str = field(default='n/a')  #
    id: str = field(default='n/a')
    phone: Optional[str] = field(default=None)
    price: Optional[str] = field(default=None)


def check_data_present(data_source_path, bar_source_path):
    if path.exists(data_source_path) and path.exists(bar_source_path):
        return
    raise IOError('Data sources should exist.')


def parse_categories(business: Dict) -> List[str]:
    if business is None:
        raise ValueError("Business should be defined.")
    return [x['alias'] for x in business['categories']]


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


def create_favorites():
    pass


def create_explored():
    pass


def create_saved_for_later():
    pass


def main():


if __name__ == '__main__':
    main()
