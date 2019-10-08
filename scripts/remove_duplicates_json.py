"""Removes duplicates in a json list"""

import json


def import_json_data(json_path):
    """Reads the json_file"""
    with open(json_path) as file_object:
        return json.load(file_object)


def write_to_json(json_path, json_data):
    """Writes data to json file"""
    with open(json_path, "w") as file_object:
        json.dump(json_data, file_object)


def remove_duplicates(data):
    """removes duplicated data in list"""
    return list(set(data))


def main():
    """main function for removing duplicates in json"""
    json_path = '../resources/database_urls.json'
    json_data = import_json_data(json_path)
    removed_duplicates = remove_duplicates(json_data)
    print(removed_duplicates)
    write_to_json(json_path, removed_duplicates)


if __name__ == "__main__":
    main()
