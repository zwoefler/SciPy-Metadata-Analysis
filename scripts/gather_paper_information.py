"""This module gathers the paper information extracted from the bookmarks"""
import argparse
import json
from selenium import webdriver
from database_classes import ScienceDirectPaper


PARAMETERS_TO_EXTRACT = [
    "title", "author", "journal", "impact factor", "citations", "publishing date"]
PAPER_INFORMATION_DICT = {}
SUPPORTED_DATABASES = ["sciencedirect", "ieeexplore"]


def read_papers_urls(url_file):
    """Reads URLs from a given json-list"""
    with open(url_file) as file_object:
        return json.load(file_object)


def write_paper_parameters_to_json(parameter_dict, export_file_name):
    """Writes the gatherd paper information dictionaries to a json file"""
    with open(export_file_name, "w") as file_object:
        json.dump(parameter_dict, file_object)


def main():
    """This is the main function thats gathers the paper
    information based on the extracted booksmarks"""


    parser = argparse.ArgumentParser(
        description='''Returns a JSON file with all the relevant meta data of an URL
        list with scientific papers from different scientific databases''',
        usage=''
    )
    parser.add_argument(
        '-u',
        '--url_json',
        type=str,
        help='Takes a URL-JSON file with a list of links',
        required='True'
    )
    parser.add_argument(
        '--s',
    )
    parser.add_argument(
        '-e',
        '--export_destination',
        type=str,
        help='export destination for the gathered meta data',
        default='paper_information.json'
    )
    args = parser.parse_args()
    url_json_file = args.url_json
    export_json_file_name = args.export_destination

    url_list = read_papers_urls(url_json_file)
    driver = webdriver.Firefox()
    scienecedirect_list = []
    for paper_url in url_list:
        driver.get(paper_url)
        scipap = ScienceDirectPaper(paper_url, driver)
        print(scipap.__dict__)
        scienecedirect_list.append(scipap.__dict__)

    PAPER_INFORMATION_DICT["ScienceDirect"] = scienecedirect_list
    write_paper_parameters_to_json(PAPER_INFORMATION_DICT, export_json_file_name)
    print("Successfully exported the paper information to", export_json_file_name)
    driver.quit()

if __name__ == "__main__":
    main()
