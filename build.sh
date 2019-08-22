# Extracts the relevant booksmarks from the JSON file
# bookmarks_file="resources/bookmarks.json"
# python3 scripts/firefox_bookmarks_from_profile.py -b "$bookmarks_file"

# Gather the Paper Metadata information from the output above
json_url_file="resources/test_urls.json"
export_json_file_name="paper_information.json"

python3 scripts/gather_paper_information.py -u "$json_url_file" -e "$export_json_file_name"