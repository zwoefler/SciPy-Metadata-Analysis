import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import argparse

json_url_file = "paper_uri_list.json"
parameters_to_extract = ["title", "author", "journal", "impact factor", "citations", "publishing date"]
paper_information_dict = {}


def read_papers_urls(url_file):
    with open(url_file) as f:
        return json.load(f)

def write_paper_parameters_to_json(parameter_dict):
    with open("paper_information.json", "w") as f:
        json.dump(parameter_dict, f)


def getTitle(articles_html):
    """Returns the title of the paper"""
    return articles_html.h1.span.text


def getAuthors(articles_html):
    """Returns the authors of the article"""
    return articles_html.


def getJournal(articles_html):
    """Returns the name of the journal were the paper has been published"""
    return


def getImpactFactor(article_html):
    """Returns the Impact factor of the journal were the paper has been published"""
    return


def getCitationsAmount(article_html):
    """Returns the amount of citations of the given paper"""
    return


def getPublishingDate(html_article):
    """Returns the Date of publishing"""
    return


def gather_information_from_page(link):
    """Returns a dictionary about the paper for ONE given link"""
    paper_information = {}
    driver = webdriver.Firefox()
    driver.get(link)
    html_page = driver.execute_script("return document.documentElement.outerHTML")

    # Create Soup Object
    soup = BeautifulSoup(html_page, 'html.parser')

    # Create articles content
    articles_content = soup.find('article')

    # Add the parameters of the paper to the paper_information dictionary
    for parameter in parameters_to_extract:
        paper_information[parameter] =
        # +++ FInd a way to reliably iterate over the already defined functions! +++
    # paper_information["title"] = getTitle(articles_content)
    # paper_information["authors"] = getAuthors(articles_content)
    # paper_information["journal"] = getJournal(soup)
    # paper_information["journal_impact_factor"] = getImpactFactor(soup)
    # paper_information["citations"] = getAmountCitations(soup)

    return paper_information


def main():
    url_list = read_papers_urls(json_url_file)
    for paper in url_list:
        paper_parameters = gather_information_from_page(url_list)
        paper_information_dict[paper_parameters["title"]] = paper_parameters


if __name__ == "__main__":
    main()

# +++ TODO +++
# Implement Argparse for:
# 1. The link to the file containing the urls of the papers

