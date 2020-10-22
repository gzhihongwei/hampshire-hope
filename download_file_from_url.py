from urllib.request import Request, urlopen
import re
from pathlib import Path
from get_links_from_webpage import get_links_from_webpage_with_headers


def download_file_from_url(url, filepath=None, filename=None):
    """
    Downloads the file from given url and saves to the given filepath as filename. If no filepath then it will just
    save to current working directory as filename. If no filename then will try to save as the filename returned by
    the http response
    :param url: http url to webpage file
    :param filepath: path to parent directory of file, will create any necessary parent directories
    :param filename: name of file with extension
    """

    fullpath = None

    if filepath:
        filepath = Path(filepath).resolve()
        filepath.mkdir(parents=True, exist_ok=True)
    else:
        filepath = Path('.').resolve()

    if filepath and filename:
        fullpath = filepath / filename

    print(f'Starting downloading file from {url}')

    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    with urlopen(request) as webpage_file:
        webpage_file_contents = webpage_file.read()

        content_disp_header_text = webpage_file.getheader('Content-Disposition')
        match = re.match(r'.*filename="(\S+)"', content_disp_header_text)

        if match and not filename and len(match.group(1)) > 0:
            filename = match.group(1)

        if filename:
            fullpath = filepath / filename
        else:
            fullpath = filepath / 'file'

    with open(fullpath, 'wb') as file:
        file.write(webpage_file_contents)

    print(f'Done downloading file from {url}')


if __name__ == '__main__':
    # download_file_from_url(
    #     'https://www.mass.gov/doc/opioid-related-overdose-deaths-among-ma-residents-june-2020/download',
    #     filepath='./mass_dot_gov_pdfs/test_dir', filename='test.pdf')

    links_dict = get_links_from_webpage_with_headers('https://www.mass.gov/lists/current-opioid-statistics',
                                                     only_download_links=True)

    for header in links_dict:
        for link_tuple in links_dict[header]:
            subject = None
            if not header:
                subject = 'No Subject'
            else:
                subject = header
            download_file_from_url(link_tuple[1], filepath=f'./mass_dot_gov_pdfs/{subject}')