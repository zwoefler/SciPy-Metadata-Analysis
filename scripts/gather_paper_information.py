"""This module gathers the paper information extracted from the bookmarks"""
import argparse
import json
from bs4 import BeautifulSoup
from selenium import webdriver

PARAMETERS_TO_EXTRACT = [
    "title", "author", "journal", "impact factor", "citations", "publishing date"]
PAPER_INFORMATION_DICT = {}


def read_papers_urls(url_file):
    """Reads URLs from a given json-list"""
    with open(url_file) as file_object:
        return json.load(file_object)


def write_paper_parameters_to_json(parameter_dict, export_file_name):
    """Writes the gatherd paper information dictionaries to a json file"""
    with open(export_file_name, "w") as file_object:
        json.dump(parameter_dict, file_object)


def get_title(article_html):
    """Returns the title of the paper"""
    return article_html.h1.span.text


def get_authors(articles_html):
    """Returns the authors of the article"""
    author_list = []
    names_list = []
    # Get the <span> Element of the authors section
    authors_spans = articles_html.findAll("span", ["given-name", "surname"])

    # Extract names and put the names as tuple in new list
    for author_span in authors_spans:
        names_list.append(author_span.text)
    author_names_set_list = list(zip(names_list[::2], names_list[1::2]))

    # Join first and surname together
    for _set in author_names_set_list:
        author_list.append(" ".join(_set))

    return author_list


def get_journal(articles_html):
    """Returns the name of the journal were the paper has been published"""
    return articles_html.find("h2", "publication-title").a.text


def get_impact_factor():
    """Returns the Impact factor of the journal were the paper has been published"""
    return


def get_citations_amount():
    """Returns the amount of citations of the given paper"""
    return


def get_publishing_date():
    """Returns the Date of publishing"""
    return


def gather_information_from_page(link, driver):
    """Returns a dictionary about the paper for ONE given link"""
    paper_information = {}
    driver.get(link)
    html_page = driver.execute_script("return document.documentElement.outerHTML")

    # Create Soup Object
    soup = BeautifulSoup(html_page, 'html.parser')

    # Create articles content
    articles_content = soup.find('article')

    # Add the parameters of the paper to the paper_information dictionary
    paper_information["title"] = get_title(articles_content)
    paper_information["authors"] = get_authors(articles_content)
    paper_information["journal"] = get_journal(articles_content)
    # paper_information["journal_impact_factor"] = getImpactFactor(soup)
    # paper_information["citations"] = getCitationsAmount(soup)

    return paper_information


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
        '--url_list',
        type=str,
        help='Takes a URL-JSON file with a list of links',
        required='True'
    )
    parser.add_argument(
        '-e',
        '--export_destination',
        type=str,
        help='export destination for the gathered meta data',
        default='paper_information.json'
    )
    args = parser.parse_args()
    url_json_file = args.url_list
    export_json_file_name = args.export_destination

    url_list = read_papers_urls(url_json_file)
    driver = webdriver.Firefox()
    for paper in url_list:
        paper_parameters = gather_information_from_page(paper, driver)
        PAPER_INFORMATION_DICT[paper_parameters["title"]] = paper_parameters

    write_paper_parameters_to_json(PAPER_INFORMATION_DICT, export_json_file_name)
    print("Successfully exported the paper information to", export_json_file_name)
    driver.quit()

if __name__ == "__main__":
    main()
