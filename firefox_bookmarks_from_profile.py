import json

bookmark_json = "bookmarks-2019-06-18.json"


def read_path_json(source_json):
    with open(source_json) as f:
        data = json.load(f)
    return data


def write_to_json(data):
    with open('paper_uri_list.json', 'w') as f:
        json.dump(data, f)


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


def main():
    bookmark_json_data = read_path_json(bookmark_json)
    papers_uri_list = extract_paper_urls(bookmark_json_data)
    write_to_json(papers_uri_list)


if __name__ == "__main__":
    main()