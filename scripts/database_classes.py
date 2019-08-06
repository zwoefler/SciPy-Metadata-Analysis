"""This module aims to provide classes to gather information for the different scientific
databases. Scince the different Research-Databases have there differences in presenting
their papers there need to be different ways of retreiving the data"""
from abc import ABCMeta, abstractmethod
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class PaperMetaData(metaclass=ABCMeta):
    """This is an abstract class for the meta information from scientific papers"""

    @abstractmethod
    def get_title(self, selenium_driver):
        """Returns the title of the paper"""


    @abstractmethod
    def get_authors(self, selenium_driver):
        """Returns the authors of the article"""


    @abstractmethod
    def get_journal_name(self, selenium_driver):
        """Returns the name of the journal were the paper has been published"""


    @abstractmethod
    def get_journal_impact_factor(self, selenium_driver):
        """Returns the Impact factor of the journal were the paper has been published"""


    @abstractmethod
    def get_citations_amount(self, selenium_driver):
        """Returns the amount of citations of the given paper"""


    @abstractmethod
    def get_publishing_date(self, selenium_driver):
        """Returns the Date of publishing"""


    @abstractmethod
    def get_paper_keyword_list(self, selenium_driver):
        """Returns a list of the given keywords or None"""


    @abstractmethod
    def get_paper_doi(self, selenium_driver):
        """Returns the DOI of the given paper"""



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
        return authors_list


    def get_journal_name(self, selenium_driver):
        """Returns the name of the journal were the paper has been published"""
        journal_name = selenium_driver.find_element(
            By.XPATH, '//*[@id="mathjax-container"]/div[2]/article/div[1]/div[2]/h2/a').text
        print(journal_name)
        return journal_name


    def get_journal_impact_factor(self, selenium_driver):
        """Returns the Impact factor of the journal were the paper has been published"""
        journal_link = selenium_driver.find_element_by_class_name("publication-title-link")
        journal_link.click()
        impact_factor = selenium_driver.find_element_by_xpath(
            '//div[@class="move-bottom u-margin-xs-bottom"]/div[2]/button/span/span[1]').text
        selenium_driver.back()
        return impact_factor


    def get_citations_amount(self, selenium_driver):
        """Returns the amount of citations of the given paper"""
        class_count = WebDriverWait(selenium_driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, """/html/body/div[3]/div/div/section/div[1]/div[2]/div[2]
                /aside/section[3]/div/div/div/div/div[2]/div[1]/div/ul/li/span[2]"""))
        )
        return class_count.text


    def get_publishing_date(self, selenium_driver):
        """Returns the Date of publishing"""

        return

    def get_paper_keyword_list(self, selenium_driver):
        """Returns a list of the given keywords or None"""
        keyword_list = []
        keyword_div = selenium_driver.find_elements_by_class_name("keyword")
        for div in keyword_div:
            keyword = div.find_element_by_tag_name("span").text
            keyword_list.append(keyword)

        return keyword_list


    def get_paper_doi(self, selenium_driver):
        """Returns the DOI of the current Paper"""
        doi_link = selenium_driver.find_element_by_class_name("doi").text
        return doi_link
