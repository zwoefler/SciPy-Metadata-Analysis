import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import argparse

json_url_file = "../resources/test_urls.json"
parameters_to_extract = ["title", "author", "journal", "impact factor", "citations", "publishing date"]
paper_information_dict = {}


def read_papers_urls(url_file):
    with open(url_file) as f:
        return json.load(f)


def write_paper_parameters_to_json(parameter_dict):
    with open("paper_information.json", "w") as f:
        json.dump(parameter_dict, f)


def getTitle(article_html):
    """Returns the title of the paper"""
    return article_html.h1.span.text


def getAuthors(articles_html):
    """Returns the authors of the article"""
    author_list = []
    names_list = []
    # Get the <span> Element of the authors section
    authors_spans = articles_html.findAll("span", ["given-name", "surname"])

    # Extract names and put the as tuple in new list
    [names_list.append(x.text) for x in authors_spans]
    author_names_set_list = list(zip(names_list[::2], names_list[1::2]))

    # Join first and surname together
    for _set in author_names_set_list:
        author_list.append(" ".join(_set))

    return author_list


def getJournal(articles_html):
    """Returns the name of the journal were the paper has been published"""
    return articles_html.find("h2", "publication-title").a.text


def getImpactFactor(article_html):
    """Returns the Impact factor of the journal were the paper has been published"""
    return


def getCitationsAmount(paper_html):
    """Returns the amount of citations of the given paper"""
    paper_html.find()
    return


def getPublishingDate(html_article):
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
    paper_information["title"] = getTitle(articles_content)
    paper_information["authors"] = getAuthors(articles_content)
    paper_information["journal"] = getJournal(articles_content)
    # paper_information["journal_impact_factor"] = getImpactFactor(soup)
    # paper_information["citations"] = getCitationsAmount(soup)

    return paper_information


def main():
    url_list = read_papers_urls(json_url_file)
    driver = webdriver.Firefox()
    for paper in url_list:
        paper_parameters = gather_information_from_page(paper, driver)
        paper_information_dict[paper_parameters["title"]] = paper_parameters

    write_paper_parameters_to_json(paper_information_dict)

if __name__ == "__main__":
    main()


# +++ TODO +++
# Implement Argparse for:
# 1. The link to the file containing the urls of the papers

