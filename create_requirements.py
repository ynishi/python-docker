import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pip._internal import main
from pip._internal.operations import freeze
from typing import Set, Tuple, List

'''
For create requiremnts.txt include popular packages
'''

conf = {
    'awesome_URL':
    'https://github.com/vinta/awesome-python/blob/master/README.md',
    'pypi_api_URL': 'https://pypi.python.org/pypi/{}/json',
    'pypi_search_URL': 'https://pypi.org/search/?q={}',
    'found_css_class': 'package-snippet__title',
    'error_pkg_str': 'failed to install',
    'found_pkg_msg': 'Found package: {}',
    'not_found_pkg_msg': 'Not found package like: {}',
    'succeeded_install_msg': 'Succeeded install package: {}',
    'failed_install_msg': 'Failed install package: {}',
    'already_installed_msg': 'Already installed package: {}',
    'requirements_filename': 'requirements.txt.auto',
}


def make_candidate() -> Set[str]:
    '''
    make candidate packages from awesome-python project.
    '''
    awesome_res = requests.get(conf['awesome_URL'])
    awesome_soup = BeautifulSoup(awesome_res.text, 'html.parser')
    return set([link.text for link in awesome_soup.select(
        'li > a') if link.get('href').startswith('http')])


def make_packages(candidate: Set[str],
                  freezed: Set[str]) -> Set[Tuple[str, bool]]:
    '''
    make valid packages from PyPI
    '''
    acc = set()
    for pkg in candidate - freezed:
        api_res = requests.head(
            conf['pypi_api_URL'].format(pkg),
            allow_redirects=True)
        if api_res.status_code == 200:
            p = urlparse(api_res.url).path.split('/')
            if len(p) > 2:
                print(conf['found_pkg_msg'].format(p[2]))
                acc.add(p[2])
            else:
                print(conf['found_pkg_msg'].format(pkg))
                acc.add(pkg)
        else:
            search_res = requests.get(
                conf['pypi_search_URL'].format(pkg),
                allow_redirects=True)
            search_soup = BeautifulSoup(search_res.text, 'html.parser')
            found = search_soup.find('h3', class_=conf['found_css_class'])
            if found is not None:
                print(conf['found_pkg_msg'].format(found.find('a').text))
                acc.add(found.find('a').text)
            else:
                print(conf['not_found_pkg_msg'].format(pkg))
    output = set([(x, True) for x in acc - freezed])
    output.update(set([(x, False) for x in freezed]))
    return output


def set2sorted(packages: Set[Tuple[str, bool]]) -> List[Tuple[str, bool]]:
    '''
    convert set to sorted list
    '''
    names_list = list(packages)
    names_list.sort(key=lambda t: t[0].lower())
    return names_list


def pkg2requirement(pkg: (str, bool)) -> str:
    '''
    make pacakge to requirement str
    '''
    if pkg[1]:
        if main(["install", pkg[0]]) == 0:
            print(conf['succeeded_install_msg'].format(pkg[0]))
            return pkg[0]
        else:
            print(conf['failed_install_msg'].format(pkg[0]))
            return '# {} # {}'.format(pkg[0], conf['error_pkg_str'])
    else:
        print(conf['already_installed_msg'].format(pkg[0]))
        return pkg[0]


def make_freezed() -> Set[str]:
    '''
    make freezed packages set
    '''
    return set([x.split('==')[0] for x in freeze.freeze()])


if __name__ == "__main__":

    candidate = make_candidate()
    freezed = make_freezed()
    packages = make_packages(candidate, freezed)
    requirements = (pkg2requirement(pakcage)
                    for pakcage in set2sorted(packages))

    with open(conf['requirements_filename'], "w") as f:
        f.write('\n'.join(requirements))
