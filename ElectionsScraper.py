import sys
import csv
import requests
from bs4 import BeautifulSoup


def main():
    link = get_link()
    write_to_csv(link)


def get_td_elements():  # get td elements
    pass


def get_soup():  # get BeautifulSoup object
    pass


def get_link():  # get a final list of values
    input_link = input('Insert URL with elections results from your desired district: ')


def write_to_csv():
    pass


def et_td_elements():
    pass


def name_of_the_csv():
    pass



def get_locations_numbers():  # get numbers of locations
    pass


def get_locations_names():  # get names of locations
    pass


def get_locations_links(): # get link to location
    pass


def get_parties_names():  # to get names of parties (ODS, ČSSD)
    pass


def make_csv_header():  # make head of tab
    pass


if __name__ == "__main__":
    main()
