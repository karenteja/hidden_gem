#!/usr/bin/env python

import argparse
from argparse import ArgumentParser
import requests as r
import json
import sys

"""
This is a CLI that uses Yelp Fusion API.
It's main purpose is to extract restaurants/bars data
based on a search term and location.
It optionally saves the extracted data too. 
"""

DEFAULT_DATA_DIRS = {
    'bars': '../data/bars.json'
}

DEFAULT_HOST = 'https://api.yelp.com'
DEFAULT_PATH = 'v3/businesses/search'
DEFAULT_SEARCH_LIMIT = 3
DEFAULT_TERM = 'bars'
DEFAULT_LOCATION = 'San Francisco, CA'


def search(host=DEFAULT_HOST, path=DEFAULT_PATH, keys=None, url_params=None):
    if not keys:
        raise ValueError('Keys are not defined.')
    api_key = keys['api_key']
    headers = {'Authorization': f'Bearer {api_key}'}
    url_params = url_params or {}
    url = f'{host}/{path}'
    try:
        response = r.request('GET', url, headers=headers, params=url_params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(e)
        sys.exit(1)


def create_url_params_list(location, term, limit):
    max_results_per_request = 50
    if limit <= max_results_per_request:
        raise ValueError("One url params is enough.")
    else:
        r = range(0, limit)
        splits = [r[i:i + max_results_per_request] for i in range(0, len(r), max_results_per_request)]
        extra_params = [{'term': term.replace(' ', '+'), 'location': location.replace(' ', '+'), 'limit': len(request),
                         'offset': request[0] + 1} for request in splits]
        return extra_params


def search_in_location(location, term, limit):
    if location is None or term is None or limit is None:
        raise ValueError("Location, term and limit should be defined.")

    if limit > 50:
        url_params_list = create_url_params_list(location, term, limit)
        return [search(keys=populate_keys(), url_params=url_params) for url_params in url_params_list]

    else:
        url_params = {
            'term': term.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': limit
        }
        return search(keys=populate_keys(), url_params=url_params)


def save_locally(data):
    if data is None:
        raise ValueError('Data should be present to save it.')

    with open(DEFAULT_DATA_DIRS['bars'], 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)
    print(f'Saved.')


def populate_keys():
    with open('key', 'r') as f:
        client_id = f.readline().split(',')[1].strip()
        api_key = f.readline().split(',')[1].strip()
        keys = {}
        keys['client_id'] = client_id
        keys['api_key'] = api_key
        return keys


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
    parser = ArgumentParser(description="Get some bar/restaurant data.")
    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str,
                        help=f'Search term, e.g. {DEFAULT_TERM}.')
    parser.add_argument('-l', '--location', dest='loc', default=DEFAULT_LOCATION, type=str,
                        help=f'Search location, e.g. {DEFAULT_LOCATION}.')
    parser.add_argument('-li', '--limit', dest='lim', default=DEFAULT_SEARCH_LIMIT, type=int,
                        help=f'Search limit, e.g. 3')
    parser.add_argument('-s', '--save', dest='save', type=str2bool, nargs='?', const=True, default=False,
                        help='Save to a local file. If false just prints data to stdout.')
    params = parser.parse_args()
    data = search_in_location(params.loc, params.term, params.lim)

    if params.lim > 900:
        raise ValueError("Can't get more than 900 locations.")
    if data is not None:
        if params.save:
            print('Saving the data')
            save_locally(data)
        else:
            print('Here is a piece of your data:')
            print(data[0]['businesses'][0])


if __name__ == '__main__':
    main()
