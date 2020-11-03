import sys
import csv
import requests
from bs4 import BeautifulSoup


def main():
    link = get_link()
    write_to_csv(link)


def get_soup(link):  # get BeautifulSoup object
    try:
        response = requests.get(link)
    except Exception as exc:
        print('There was a problem: {}'.format(exc))
        sys.exit()
    return BeautifulSoup(response.text, 'html.parser')


def get_link():  # get a final list of values
    input_link = input('Insert URL with elections results from your desired district: ').strip()
    soup = get_soup(input_link)
    locations_numbers = get_locations_numbers(soup)
    locations_names = get_locations_names(soup)
    locations_links = get_locations_links(soup)
    return list(zip(locations_numbers, locations_names, locations_links))


def write_to_csv(locations_list):
    filename = input('Specify name of your file (without suffix): ').strip()
    link = 'https://www.volby.cz/pls/ps2017nss/' + locations_list[0][2]
    header_soup = get_soup(link)
    header = make_csv_header(header_soup)
    with open('{}.csv'.format(filename), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for location in locations_list:
            print('Currently processing location {}.'.format(location[1]))
            link = 'https://www.volby.cz/pls/ps2017nss/' + location[2]
            soup = get_soup(link)
            results = get_location_results(soup)
            writer.writerow([location[0], location[1]] + results)


def get_location_results(soup_obj):
    return get_info_values(soup_obj) + get_parties_votes(soup_obj)


def get_info_values(soup_obj):
    info_headers = ['sa2', 'sa3', 'sa6']
    info_values = []
    for info_header in info_headers:
        value_element = soup_obj.find('td', {'headers': '{}'.format(info_header)})
        value_element = value_element.text
        value_element = value_element.replace('\xa0', '')
        info_values.append(int(value_element))
    return info_values


def get_td_elements(soup_obj, *args):
    elements = []
    for arg in args:
        elements += soup_obj.select('td[headers="{}"]'.format(arg))
    return elements


def get_locations_numbers(soup_obj):  # get numbers of locations
    td_elements = get_td_elements(soup_obj, 't1sa1 t1sb1', 't2sa1 t2sb1', 't3sa1 t3sb1')
    td_numbers = []
    for td in td_elements:
        if td.find('a'):
            anchor_element = td.find('a')
            td_numbers.append(anchor_element.text)
    return td_numbers


def get_locations_names(soup_obj):  # get names of locations
    td_elements = get_td_elements(soup_obj, 't1sa1 t1sb2', 't2sa1 t2sb2', 't3sa1 t3sb2')
    return [td.text for td in td_elements]


def get_locations_links(soup_obj):  # get link to location
    td_elements = get_td_elements(soup_obj, 't1sa1 t1sb1', 't2sa1 t2sb1', 't3sa1 t3sb1')
    td_links = []
    for td in td_elements:
        if td.find('a'):
            anchor_element = td.find('a')
            td_links.append(anchor_element.get('href'))
    return td_links


def get_parties_names(soup_obj):  # to get names of parties (ODS, ČSSD)
    elements = get_td_elements(soup_obj, 't1sa1 t1sb2', 't2sa1 t2sb2')
    return [element.text for element in elements if element.text != '-']


def make_csv_header(soup_obj):  # make head of tab
    info = ['code', 'location', 'registered', 'envelopes', 'valid']
    parties_names = get_parties_names(soup_obj)
    return info + parties_names


def get_parties_votes(soup_obj):
    elements = get_td_elements(soup_obj, 't1sa2 t1sb3', 't2sa2 t2sb3')
    parties_votes = []
    for element in elements:
        if element.text != '-':
            element = element.text.replace('\xa0', '')
            parties_votes.append(int(element))
    return parties_votes


if __name__ == "__main__":
    main()
