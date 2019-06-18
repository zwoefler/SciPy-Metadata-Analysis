import os
import sqlite3
import json
import pandas as pd

json_paths = "paths_and_data.json"
bookmark_json = "bookmarks-2019-06-18.json"

def read_path_json(source_json):
    with open(source_json) as f:
        data = json.load(f)
    return data

def extract_firefox_profile_path(data):
    """Extracts the firefox profile path out of the given json that contains important paths"""
    firefox_profile_path = data["firefox_profile_path"]
    print("Your firefox profile path is: \n" + firefox_profile_path)
    return firefox_profile_path

def execute_query(cursor, query):
    try:
        cursor.execute(query)
    except Exception as error:
        print(str(error) + "\n" + query)


def get_bookmarks(cursor):
    bookmarks_query = """select url, moz_places.title, rev_host, frecency,
    last_visit_date from moz_places  join  \
    moz_bookmarks on moz_bookmarks.fk=moz_places.id where visit_count>0
    and moz_places.url  like 'http%'
    order by dateAdded desc;"""
    execute_query(cursor, bookmarks_query)
    for row in cursor:
        link = row[0]
        title = row[1]
        print(link,title)

    return


def main():
    json_data = read_path_json(json_paths)
    firefox_profile_path = extract_firefox_profile_path(json_data)
    sql_bookmarks_path = os.path.join(firefox_profile_path, sql_bookmarks_file)
    print(sql_bookmarks_path)
    if os.path.exists(sql_bookmarks_path):
        firefox_connection = sqlite3.connect(sql_bookmarks_path)
    cursor = firefox_connection.cursor()
    get_bookmarks(cursor)
    cursor.close





if __name__ == "__main__":
    main()