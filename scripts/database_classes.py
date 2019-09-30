"""This module aims to provide classes to gather information for the different scientific
databases. Scince the different Research-Databases have there differences in presenting
their papers there need to be different ways of retreiving the data"""
# pylint: disable=too-many-instance-attributes

from abc import ABCMeta, abstractmethod
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

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

    def __init__(self, url, selenium_driver):
        """Initializes the ScienceDirectPaper object"""
        self.url = url
        self.title = self.get_title(selenium_driver)
        self.authors = self.get_authors(selenium_driver)
        self.journal = self.get_journal_name(selenium_driver)
        self.journal_impact_factor = self.get_journal_impact_factor(selenium_driver)
        self.citations = self.get_citations_amount(selenium_driver)
        self.publish_date = self.get_publishing_date(selenium_driver)
        self.keywords = self.get_paper_keyword_list(selenium_driver)
        self.doi = self.get_paper_doi(selenium_driver)


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
                (By.XPATH, """//*[@id="mathjax-container"]/div[2]/div[2]
                /aside/section[3]/div/div/div/div/div[2]/div[1]/div/ul/li/span[2]"""))
        )
        return class_count.text


    def get_publishing_date(self, selenium_driver):
        """Returns the Date of publishing"""
        publishing_info_div = '//*[@id="mathjax-container"]/div[2]/article/div[1]/div[2]/div'
        publishing_info_text = selenium_driver.find_element_by_xpath(publishing_info_div).text
        publish_date = publishing_info_text.split(',')[1].strip()
        #Regex also possible
        publish_year = publish_date.split(' ')[1]
        return publish_year

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


class IEEEPaper(PaperMetaData):
    """Extract Meta Information from IEEE-Explore database papers"""

    def __init__(self, url, selenium_driver):
        """Initializes the IEEEPaper object"""
        self.url = url
        self.title = self.get_title(selenium_driver)
        self.authors = self.get_authors(selenium_driver)
        self.journal = self.get_journal_name(selenium_driver)
        self.journal_impact_factor = self.get_journal_impact_factor(selenium_driver)
        self.citations = self.get_citations_amount(selenium_driver)
        # self.publish_date = self.get_publishing_date(selenium_driver)
        # self.keywords = self.get_paper_keyword_list(selenium_driver)
        # self.doi = self.get_paper_doi(selenium_driver)


    def get_title(self, selenium_driver):
        """Returns the title of the paper"""
        title_div = selenium_driver.find_element(
            By.CLASS_NAME,
            "document-title")
        title_text = title_div.find_element(By.TAG_NAME, "span").text
        return title_text


    def get_authors(self, selenium_driver):
        """Returns the authors of the article"""
        author_spans = selenium_driver.find_elements(
            By.XPATH,
            "//span[@class='authors-info']"
        )
        for author in author_spans:
            print(author.text)
        return 0

    @staticmethod
    def get_journal_link(selenium_driver):
        """Returns the link, pointing to the Journalname"""
        published_in_div = selenium_driver.find_element(
            By.XPATH,
            "//div[@class='u-pb-1 stats-document-abstract-publishedIn']"
        )
        journal_link = published_in_div.find_element(
            By.TAG_NAME,
            "a")
        return journal_link


    def get_journal_name(self, selenium_driver):
        """Returns the name of the journal were the paper has been published"""
        journal_name = self.get_journal_link(selenium_driver).text
        return journal_name


    def get_journal_impact_factor(self, selenium_driver):
        """Returns the Impact factor of the journal were the paper has been published"""
        # Try except for when the jiournal is a conference paper
        # pylint: disable=pointless-statement
        # Pylint think *.location_once_scrolled_into_view is pointless

        impact_factor = None
        journal_link = self.get_journal_link(selenium_driver)
        journal_link.location_once_scrolled_into_view
        journal_link.click()

        try:
            impact_factor_link = WebDriverWait(selenium_driver, 3).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//a[@class='stats-jhp-impact-factor']"))
            )
            impact_factor_link.location_once_scrolled_into_view
            impact_factor = impact_factor_link.text.split()[0]

        except TimeoutException as exception:
            # Papers without an impact factor are getting cought
            print(
                "Could not find the impact factor on site:",
                selenium_driver.current_url, exception)

        selenium_driver.back()
        return impact_factor


    def get_citations_amount(self, selenium_driver):
        """Returns the amount of citations of the given paper"""
        citations_div = selenium_driver.find_element(
            By.CLASS_NAME,
            "document-banner-metric-count")
        citations_amount = citations_div.text
        return citations_amount


    def get_publishing_date(self, selenium_driver):
        """Returns the Date of publishing"""
        publishing_date_div = selenium_driver.find_element(
            By.CLASS_NAME,
            "u-pb-1 doc-abstract-pubdate")
        publishing_date = publishing_date_div.text
        return publishing_date


    def get_paper_keyword_list(self, selenium_driver):
        """Returns a list of the given keywords or None"""
        return 0


    def get_paper_doi(self, selenium_driver):
        """Returns the DOI of the given paper"""
        return 0
