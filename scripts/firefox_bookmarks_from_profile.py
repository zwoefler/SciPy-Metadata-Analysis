"""Extracts the the relevant booksmarks of a firefox library"""
import json
import os
import argparse


def read_path_json(source_json):
    """Reads the data of a given json file"""
    with open(source_json) as file:
        data = json.load(file)
    return data


def write_to_json(data):
    """Writes the list of paper URLs to a json file"""
    with open('paper_uri_list.json', 'w') as file:
        json.dump(data, file)


def extract_paper_urls(data):
    """This function cycles through the bookmarks and returns a list with the URLs for the papers"""
    source_folders_list = []
    paper_uri_list = []
    folder_with_sources = data["children"][2]["children"][17]["children"][14]
    for datum in folder_with_sources["children"]:
        if "children" in datum:
            source_folders_list.append(datum)

    for folder in source_folders_list:
        for item in folder["children"]:
            paper_uri_list.append(item["uri"])
    return paper_uri_list


# +++ Implement argparse +++
# ===Argparse===


def main():
    """The main function"""
    data_dir = "resources"

    parser = argparse.ArgumentParser(
        description='Returns a list of all found scientific papers in the bookmarks',
        usage=''
    )
    parser.add_argument(
        '-b',
        '--bookmarks',
        type=str,
        help='Path to the bookmark source file to extract the booksmarks from',
        required='True'
    )
    parser.add_argument(
        '-d',
        '--destination',
        type=str,
        help='export destination for all scripts',
        default=os.path.join(data_dir, 'paper_uri_list.json')
    )
    args = parser.parse_args()
    bookmark_json = args.bookmarks
    bookmark_json_data = read_path_json(bookmark_json)
    papers_uri_list = extract_paper_urls(bookmark_json_data)
    write_to_json(papers_uri_list)
    print("Successfully extracted the relevant booksmarks into paper_uri_list.json")


if __name__ == "__main__":
    main()
