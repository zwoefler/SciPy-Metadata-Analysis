"""This module gathers the paper information extracted from the bookmarks"""
import argparse
import json
from selenium import webdriver
from database_classes import IEEEPaper, ScienceDirectPaper

JSON_EXPORT_LIST = []


def read_papers_urls(url_file):
    """Reads URLs from a given json-list"""
    with open(url_file) as file_object:
        return json.load(file_object)


def write_paper_parameters_to_json(parameter_dict, export_file_name):
    """Writes the gatherd paper information dictionaries to a json file"""
    with open(export_file_name, "w") as file_object:
        json.dump(parameter_dict, file_object)


def get_scientific_database_name(link):
    """Returns the scientific database used, by extracting it from the link"""
    supported_databases = ["sciencedirect", "ieeexplore"]
    for db in supported_databases:
        if db in link:
            db_name = db
            break
    return db_name


def switch_function_selecting_db_class(db, link, driver):
    """This function works as a switcher, selecting the correct databaseclass
    to extract the corret meta information"""
    if db == "ieeexplore":
        paper_info_obj = IEEEPaper(link, driver)
    if db == "sciencedirect":
        paper_info_obj = ScienceDirectPaper(link, driver)

    return paper_info_obj


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

    for paper_url in url_list:
        driver.get(paper_url)
        db = get_scientific_database_name(paper_url)
        scipaper_obj = switch_function_selecting_db_class(db, paper_url, driver)
        print(scipaper_obj.__dict__)
        JSON_EXPORT_LIST.append(scipaper_obj.__dict__)

    write_paper_parameters_to_json(JSON_EXPORT_LIST, export_json_file_name)
    print("Successfully exported the paper information to", export_json_file_name)
    driver.quit()

if __name__ == "__main__":
    main()
