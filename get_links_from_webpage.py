import requests
from requests_html import HTMLSession
from html.parser import HTMLParser
import re
from collections import deque

EXAMPLE_HTML_FROM_MASS_DOT_GOV = '<div class="ma__download-link ">' \
                                 '   <div class="ma__download-link__icon">' \
                                 '       <svg aria-hidden="true" focusable="false">' \
                                 '           <use xlink:href="#08b07eb0f896963fa2703861933b865e"></use>' \
                                 '       </svg>' \
                                 '   </div>' \
                                 '   <div class="ma__download-link__title">' \
                                 '       <a class="ma__download-link__file-link" href="https://www.mass.gov/doc/opioid-related-overdose-deaths-among-ma-residents-june-2020/download"> ' \
                                 '           <span class="visually-hidden">Open PDF file, 239.35 KB, for</span>' \
                                 '           Opioid-related Overdose Deaths among MA Residents - June 2020' \
                                 '       </a>' \
                                 '       <span class="ma__download-link__file-spec">(PDF 239.35 KB)</span>' \
                                 '   </div>' \
                                 '</div>'


class MyHTMLParser(HTMLParser):
    def __init__(self, only_download_links):
        """
        Class from html.parser package used to parse html text
        :param only_download_links: if true then self.links is only filled with links that end in "download"
        """
        super().__init__()

        self.links = {}
        self.current_link = None
        self.current_header = None
        self.header_tags = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}
        self.tags_within_anchor_tag_stack = deque()
        self.inside_header_tag = False
        self.inside_anchor_tag = False
        self.only_download_links = only_download_links

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)

        # set self.inside_header_tag to true so that when self.handle_data() is called next
        # it knows that the data is header text
        if tag in self.header_tags:
            self.inside_header_tag = True

        # if parsing an anchor tag set self.inside_anchor_tag to true and get link from attrs list
        if not self.inside_anchor_tag:
            if tag == 'a':
                self.inside_anchor_tag = True
                for attribute in attrs:
                    if attribute[0] == 'href':
                        self.current_link = attribute[1]
        # if not parsing and anchor tag but inside of one then add the tag to self.tags_within_anchor_tag_stack
        # so that when self.handle_data() is called next it is known that the data is not the text data associated
        # with the link of the anchor tag, example of this type of scenario in EXAMPLE_HTML_FROM_MASS_DOT_GOV
        else:
            self.tags_within_anchor_tag_stack.append(tag)

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)

        if tag in self.header_tags:
            self.inside_header_tag = False

        if tag == 'a':
            self.inside_anchor_tag = False
            self.current_link = None
        else:
            if len(self.tags_within_anchor_tag_stack) > 0:
                self.tags_within_anchor_tag_stack.pop()

    def handle_data(self, data):
        # print(f"Encountered some data (len={len(data.strip())}) :", data)

        data = data.strip()

        if self.inside_header_tag:
            self.current_header = data

        # if inside of an anchor tag and not within any tags nested within the last anchor (indicated by
        # len(self.tags_within_anchor_tag_stack) == 0) tag then this data is the text associated with the
        # link from the last anchor tag
        if self.inside_anchor_tag and len(self.tags_within_anchor_tag_stack) == 0:
            if len(data) > 0 and (not self.only_download_links or (
                    self.only_download_links and self.current_link.endswith('download'))):

                if self.current_header not in self.links:
                    self.links[self.current_header] = []

                self.links[self.current_header].append((data, self.current_link))


def get_all_download_links(page_url):
    session = HTMLSession()
    response = session.get(page_url)

    all_links = response.html.links

    download_links = []
    for link in all_links:
        if link.endswith('download'):
            download_links.append(link)

    return download_links


def get_links_from_webpage_with_headers(page_url, only_download_links=False):
    response = requests.get(page_url)
    parser = MyHTMLParser(only_download_links)
    # parser.feed(EXAMPLE_HTML_FROM_MASS_DOT_GOV)
    parser.feed(response.text)
    links_dict = parser.links
    return links_dict


if __name__ == '__main__':
    # print(get_all_download_links('https://www.mass.gov/lists/current-opioid-statistics'))
    links_dict = get_links_from_webpage_with_headers('https://www.mass.gov/lists/current-opioid-statistics',
                                                     only_download_links=False)
    for header in links_dict:
        print(f'{len(links_dict[header])} links with parent header "{header}"')
        for link_tuple in links_dict[header]:
            print('\t', link_tuple)