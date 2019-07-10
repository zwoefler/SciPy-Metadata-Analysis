"""This module aims to provide classes to gather information for the different scientific
databases. Scince the different Research-Databases have there differences in presenting
their papers there need to be different ways of retreiving the data"""

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





class ScienceDirectPaper(PaperMetaData):
    """Extract Meta Information from ScienceDirect Papers"""

    def get_title(self, article_html):
        """Returns the title of the paper"""
        return article_html.h1.span.text


    def get_authors(self, articles_html):
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


    def get_journal(self, articles_html):
        """Returns the name of the journal were the paper has been published"""
        return articles_html.find("h2", "publication-title").a.text


    def get_impact_factor(self):
        """Returns the Impact factor of the journal were the paper has been published"""
        return


    def get_citations_amount(self):
        """Returns the amount of citations of the given paper"""
        return


    def get_publishing_date(self):
        """Returns the Date of publishing"""
        return
