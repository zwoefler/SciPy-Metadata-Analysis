"""This module aims to provide classes to gather information for the different scientific
databases. Scince the different Research-Databases have there differences in presenting
their papers there need to be different ways of retreiving the data"""
# pylint: disable=too-many-instance-attributes


from abc import ABCMeta, abstractmethod
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re

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
        self.database = "sciencedirect"
        self.url = url
        self.title = self.get_title(selenium_driver)
        self.authors = self.get_authors(selenium_driver)
        self.journal = self.get_journal_name(selenium_driver)
        self.citations = self.get_citations_amount(selenium_driver)
        self.publish_date = self.get_publishing_date(selenium_driver)
        self.keywords = self.get_paper_keyword_list(selenium_driver)
        self.doi = self.get_paper_doi(selenium_driver)
        self.journal_impact_factor = self.get_journal_impact_factor(selenium_driver)


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
        return journal_name


    def get_citations_amount(self, selenium_driver):
        """Returns the amount of citations of the given paper"""
        try:
            citations_count = WebDriverWait(selenium_driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, """//*[@id="mathjax-container"]/div[2]/div[2]
                    /aside/section[3]/div/div/div/div/div[2]/div[1]/div/ul/li/span[2]"""))
                ).text
        except TimeoutException as exception:
            citations_count = None
            print("Could not find the citations",
                  exception)
        return citations_count


    def get_publishing_date(self, selenium_driver):
        """Returns the Date of publishing"""
        publishing_info_text = selenium_driver.find_element(
            By.XPATH,
            "//div[@class='text-xs']").text
        publish_date = publishing_info_text.split(',')[1].strip()
        #Regex also possible
        if len(publish_date) == 4:
            publish_year = publish_date
        else:
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


    def get_journal_impact_factor(self, selenium_driver):
        """Returns the Impact factor of the journal were the paper has been published"""
        try:
            journal_link = selenium_driver.find_element(
                By.XPATH,
                "//a[@class='publication-title-link']")
            journal_link.click()
            impact_factor = selenium_driver.find_element_by_xpath(
                '//div[@class="move-bottom u-margin-xs-bottom"]/div[2]/button/span/span[1]').text
        except NoSuchElementException as exception:
            impact_factor = None
            print("Could not find the Impact factor for",
                  exception)


        selenium_driver.back()
        return impact_factor


class IEEEPaper(PaperMetaData):
    """Extract Meta Information from IEEE-Explore database papers"""

    def __init__(self, url, selenium_driver):
        """Initializes the IEEEPaper object"""
        self.database = "ieeexplore"
        self.url = url
        self.title = self.get_title(selenium_driver)
        self.authors = self.get_authors(selenium_driver)
        self.journal = self.get_journal_name(selenium_driver)
        self.citations = self.get_citations_amount(selenium_driver)
        self.publish_date = self.get_publishing_date(selenium_driver)
        self.keywords = self.get_paper_keyword_list(selenium_driver)
        self.doi = self.get_paper_doi(selenium_driver)
        self.journal_impact_factor = self.get_journal_impact_factor(selenium_driver)


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

        authors_list = [author.text.strip() for author in author_spans]
        return authors_list


    @staticmethod
    def get_journal_link(selenium_driver):
        """Returns the link, pointing to the Journalname"""
        # pylint: disable=pointless-statement
        try:
            published_in_div = selenium_driver.find_element(
                By.XPATH,
                "//div[@class='u-pb-1 stats-document-abstract-publishedIn']"
                )
            published_in_div.location_once_scrolled_into_view
            journal_link = published_in_div.find_element(
                By.TAG_NAME,
                "a")
        except NoSuchElementException as exception:
            journal_link = None
            print("Can not find the journal link. Maybe your source isn't a scientific paper? \n",
                  exception)
        return journal_link


    def get_journal_name(self, selenium_driver):
        """Returns the name of the journal were the paper has been
        published. If it isn't a proper journal, it will return
        'NaJ' for 'Not a Journal'"""
        journal_link = self.get_journal_link(selenium_driver)
        if journal_link is not None:
            journal_name = journal_link.text
        else:
            journal_name = "NaJ"
        return journal_name


    def get_citations_amount(self, selenium_driver):
        """Returns the amount of citations of the given paper"""
        citations_div = selenium_driver.find_element(
            By.CLASS_NAME,
            "document-banner-metric-count")
        citations_amount = citations_div.text
        return citations_amount


    def get_publishing_date(self, selenium_driver):
        """Returns the year of publication of teh paper"""
        publishing_year = None
        try:
            publishing_date_text = selenium_driver.find_element(
                By.XPATH,
                "//div[@class='u-pb-1 doc-abstract-pubdate']"
                ).text
        except NoSuchElementException as exception:
            try:
                publishing_date_text = selenium_driver.find_element(
                    By.XPATH,
                    "//div[@class='u-pb-1 doc-abstract-confdate']"
                ).text
            except NoSuchElementException as exception:
                publishing_date_text = None
                print("Could not find the paper publishing date for \n",
                      selenium_driver.current_url,
                      "Maybe the site is broken \n",
                      exception)
        if publishing_date_text is not None:
            publishing_year = publishing_date_text.split()[-1:][0]
        return publishing_year


    def get_paper_keyword_list(self, selenium_driver):
        """Returns a list of the given keywords or None"""
        # pylint: disable=pointless-statement

        keywords = []
        keyword_expand_button = selenium_driver.find_element(
            By.XPATH,
            "//div[@id='keywords-header']"
        )
        keyword_expand_button.location_once_scrolled_into_view
        keyword_expand_button.click()
        keyword_sections = keyword_expand_button.find_elements(
            By.XPATH,
            "//li[@class='doc-keywords-list-item']"
        )

        for section in keyword_sections:
            section_header = section.find_element(By.TAG_NAME, "strong").text
            if section_header in ["IEEE Keywords", "Author Keywords"]:
                keyword_list = section.find_elements(
                    By.XPATH,
                    ".//a[@class='stats-keywords-list-item']")
                keywords.extend([keyword.text for keyword in keyword_list])
        return keywords


    def get_paper_doi(self, selenium_driver):
        """Returns the DOI of the given paper"""
        try:
            doi_div_elem = selenium_driver.find_element(
                By.XPATH,
                "//div[@class='u-pb-1 stats-document-abstract-doi']")
            doi = doi_div_elem.find_element(By.TAG_NAME, "a").text
        except NoSuchElementException as exception:
            doi = None
            print("Could not find the doi, probably an IEEE conference paper \n",
                  exception)
        return doi


    def get_journal_impact_factor(self, selenium_driver):
        """Returns the Impact factor of the journal were the paper has been published"""
        # Try except for when the journal is a conference paper
        # pylint: disable=pointless-statement
        # Pylint think *.location_once_scrolled_into_view is pointless

        impact_factor = None
        journal_link = self.get_journal_link(selenium_driver)
        if journal_link is None:
            return impact_factor
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
                "Probably a conferencepaper, could not find the impact factor on site:",
                exception)

        return impact_factor


class SpringerLinkPaper(PaperMetaData):
    """Extract Meta Information from SpringerLink papers"""

    def __init__(self, url, selenium_driver):
        self.database = "springerlink"
        self.url = url
        self.title = self.get_title(selenium_driver)
        self.authors = self.get_authors(selenium_driver)
        self.journal = self.get_journal_name(selenium_driver)
        self.citations = self.get_citations_amount(selenium_driver)
        self.publish_date = self.get_publishing_date(selenium_driver)
        self.keywords = self.get_paper_keyword_list(selenium_driver)
        self.doi = self.get_paper_doi(selenium_driver)
        self.journal_impact_factor = self.get_journal_impact_factor(selenium_driver)


    def get_title(self, selenium_driver):
        """Returns the title of the paper"""
        title_div = selenium_driver.find_element(
            By.CLASS_NAME,
            "MainTitleSection"
        )
        title_text = title_div.find_element(
            By.TAG_NAME,
            "h1"
        ).text
        return title_text


    def get_authors(self, selenium_driver):
        """Returns the authors of the article as a list"""
        authors = []
        authors_div = selenium_driver.find_element(
            By.CLASS_NAME,
            "authors__list"
        )
        authors_names = authors_div.find_elements(
            By.CLASS_NAME,
            "authors__name"
        )
        authors = [author.text for author in authors_names]
        return authors


    @staticmethod
    def get_journal_link(selenium_driver):
        """Return the link to a journal/book. Usually it also
        consists of the exact name of the journal"""
        journal_info_div = selenium_driver.find_element(
            By.CLASS_NAME,
            "enumeration"
        )
        journal_link = journal_info_div.find_element(
            By.TAG_NAME,
            "a"
        )
        return journal_link


    def get_journal_name(self, selenium_driver):
        """Returns the name of the journal were the paper has been published"""
        # Finds the first link in the enumeration div, which corresponds to
        # the journal name
        journal_name = self.get_journal_link(selenium_driver).text
        return journal_name


    def get_journal_impact_factor(self, selenium_driver):
        """Returns the Impact factor of the journal were the paper has been published"""
        impact_factor = None
        self.get_journal_link(selenium_driver).click()

        try:
            impact_factor = selenium_driver.find_element(
                By.XPATH,
                "/html/body/div[4]/div[3]/div/div[2]/div/div[2]/div[2]/ul/li[1]/span[2]"
                ).text
        except NoSuchElementException as exception:
            impact_factor = None
            print("Could not find the Impact factor for",
                exception)
        selenium_driver.back()

        return impact_factor


    def get_citations_amount(self, selenium_driver):
        """Returns the amount of citations of the given paper"""
        citations = None

        try:
            citations= selenium_driver.find_element(
                By.XPATH,
                "//span[@id='citations-count-number']"
            ).text
            print("print it")
        except NoSuchElementException as exception:
            print("Could not find the amount of citations",
            exception)

        return citations


    def get_publishing_date(self, selenium_driver):
        """Returns the Date of publishing. Finds the Regex of four
        digits in brackets in the 'Cite as' text"""
        pub_year_regex = re.compile("\((\d{4})\)")

        cite_text = selenium_driver.find_element(
            By.ID,
            "citethis-text"
        ).text

        year_in_brackets = pub_year_regex.search(cite_text)
        pub_year = year_in_brackets.group().strip('()')

        return pub_year



    def get_paper_keyword_list(self, selenium_driver):
        """Returns a list of the given keywords or None"""
        keywords_list = selenium_driver.find_elements(
            By.XPATH,
            "//span[@class='Keyword']"
        )

        return [keyword.text.strip() for keyword in keywords_list]

    def get_paper_doi(self, selenium_driver):
        """Returns the DOI of the given paper"""
        paper_doi = selenium_driver.find_element(
            By.XPATH,
            '//*[@id="doi-url"]'
        ).text
        return paper_doi