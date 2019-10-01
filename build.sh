# Extracts the relevant booksmarks from the JSON file

# Gather the Paper Metadata information from the output above
json_url_file="resources/test_urls.json"
export_json_file_name="test_url_output.json"

python3 scripts/gather_paper_information.py -u "$json_url_file" -e "$export_json_file_name"