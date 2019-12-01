#!/usr/local/bin/python3

import sys
import os
from os import path
import json



DEFAULT_PEOPLE_SOURCE = '../data/people.json'
DEFAULT_BAR_SOURCE = '../data/bars.json'


def check_data_present(data_source_path, bar_source_path):
	if path.exists(data_source_path) and path.exists(bar_source_path):
		return
	raise IOError('Data sources should exist.')


def main():
	print("LOL")

if __name__ == '__main__':
    main()