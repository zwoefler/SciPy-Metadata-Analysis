"""This module gathers the paper information extracted from the bookmarks"""
import json
from bs4 import BeautifulSoup
from selenium import webdriver

JSON_URL_FILE = "../resources/test_urls.json"
PARAMETERS_TO_EXTRACT = [
    "title", "author", "journal", "impact factor", "citations", "publishing date"]
PAPER_INFORMATION_DICT = {}
EXPORT_JSON_FILE_NAME = "paper_information.json"


def read_papers_urls(url_file):
    """Reads URLs from a given json-list"""
    with open(url_file) as file_object:
        return json.load(file_object)


def write_paper_parameters_to_json(parameter_dict):
    """Writes the gatherd paper information dictionaries to a json file"""
    with open(EXPORT_JSON_FILE_NAME, "w") as file_object:
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
    pass


def get_citations_amount():
    """Returns the amount of citations of the given paper"""
    pass


def get_publishing_date():
    """Returns the Date of publishing"""
    pass


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
    url_list = read_papers_urls(JSON_URL_FILE)
    driver = webdriver.Firefox()
    for paper in url_list:
        paper_parameters = gather_information_from_page(paper, driver)
        PAPER_INFORMATION_DICT[paper_parameters["title"]] = paper_parameters

    write_paper_parameters_to_json(PAPER_INFORMATION_DICT)
    print("Successfully exported the paper information to", EXPORT_JSON_FILE_NAME)
    driver.quit()

if __name__ == "__main__":
    main()


# +++ TODO +++
# Implement Argparse for:
# 1. The link to the file containing the urls of the papers
