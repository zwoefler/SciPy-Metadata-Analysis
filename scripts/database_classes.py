"""This module aims to provide classes to gather information for the different scientific
databases. Scince the different Research-Databases have there differences in presenting
their papers there need to be different ways of retreiving the data"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from abc import ABCMeta, abstractmethod

class PaperMetaData(metaclass=ABCMeta):
    """This is an abstract class for the meta information from scientific papers"""

    @abstractmethod
    def get_title(self):
        """Returns the title of the paper"""
        pass


    @abstractmethod
    def get_authors(self):
        """Returns the authors of the article"""


    @abstractmethod
    def get_journal(self):
        """Returns the name of the journal were the paper has been published"""
        pass


    @abstractmethod
    def get_impact_factor(self):
        """Returns the Impact factor of the journal were the paper has been published"""
        pass


    @abstractmethod
    def get_citations_amount(self):
        """Returns the amount of citations of the given paper"""
        pass


    @abstractmethod
    def get_publishing_date(self):
        """Returns the Date of publishing"""
        pass


    @abstractmethod
    def get_paper_keyword_list(self):
        """Returns a list of the given keywords or None"""
        pass



class ScienceDirectPaper(PaperMetaData):
    """Extract Meta Information from ScienceDirect Papers"""

    def get_title(self, selenium_driver):
        """Returns the title of the paper"""
        title = selenium_driver.find_element(By.CLASS_NAME, "title-text").text
        return title


    def get_authors(self, selenium_driver):
        """Returns the authors of the article"""
        authors_list = []
        author_div = selenium_driver.find_elements(By.ID, "author-group")
        for author_link_element in author_div:
            for author_span in author_link_element.find_elements(By.TAG_NAME, "a"):
                span_context = author_span.find_element(By.TAG_NAME, "span")
                first_name = span_context.find_element(By.CLASS_NAME, "given-name").text
                surname = span_context.find_element(By.CLASS_NAME, "surname").text
                author_dict = {
                    "surname": surname,
                    "first_name": first_name
                }
                authors_list.append(author_dict)
        print(authors_list)
        return authors_list


    def get_journal(self, articles_html):
        """Returns the name of the journal were the paper has been published"""
        return


    def get_impact_factor(self):
        """Returns the Impact factor of the journal were the paper has been published"""
        return


    def get_citations_amount(self, selenium_driver):
        """Returns the amount of citations of the given paper"""
        class_count = WebDriverWait(selenium_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/section/div[1]/div[2]/div[2]/aside/section[3]/div/div/div/div/div[2]/div[1]/div/ul/li/span[2]"))
        )
        return class_count.text


    def get_publishing_date(self, ):
        """Returns the Date of publishing"""
        return

    def get_paper_keyword_list(self, soup_object):
        """Returns a list of the given keywords or None"""
