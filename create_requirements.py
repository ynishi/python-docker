import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pip._internal import main

conf = {
    'awesome_URL':
    'https://github.com/vinta/awesome-python/blob/master/README.md',
    'pypi_api_URL': 'https://pypi.python.org/pypi/{}/json',
    'pypi_search_URL': 'https://pypi.org/search/?q={}',
    'found_css_class': 'package-snippet__title',
    'error_pkg_str': 'error occurred',
    'found_pkg_msg': 'Found package: {}',
    'succeeded_install_msg': 'Succeeded install package: {}',
    'failed_install_msg': 'Failed install package: {}',
    'requirements_filename': 'requirements.txt.auto',
}

# create package list from awesome-python project.


def make_candidate():
    awesome_res = requests.get(conf['awesome_URL'])
    awesome_soup = BeautifulSoup(awesome_res.text, 'html.parser')
    return set([link.text for link in awesome_soup.select(
        'li > a') if link.get('href').startswith('http')])

# search pip package name from PyPI


def make_package_names(packages):
    output = set()
    for pkg in packages:
        api_res = requests.head(
            conf['pypi_api_URL'].format(pkg),
            allow_redirects=True)
        if api_res.status_code == 200:
            p = urlparse(api_res.url).path.split('/')
            if len(p) > 2:
                print(conf['found_pkg_msg'].format(p[2]))
                output.add(p[2])
            else:
                print(conf['found_pkg_msg'].format(pkg))
                output.add(pkg)
        else:
            search_res = requests.get(
                conf['pypi_search_URL'].format(pkg),
                allow_redirects=True)
            search_soup = BeautifulSoup(search_res.text, 'html.parser')
            found = search_soup.find('h3', class_=conf['found_css_class'])
            if found is not None:
                print(conf['found_pkg_msg'].format(found.find('a').text))
                output.add(found.find('a').text)
    return output

# convert set to sorted list


def set2sorted(s):
    res_list = list(s)
    res_list.sort(key=lambda k: k.lower())
    return res_list

# pacakge name to requirements


def pkg2requirement(pkg: str) -> str:
    if main(["install", pkg]) == 0:
        print(conf['succeeded_install_msg'].format(pkg))
        return pkg
    else:
        print(conf['failed_install_msg'].format(pkg))
        return '# {} # {}'.format(pkg, conf['error_pkg_str'])


if __name__ == "__main__":
    candidate = make_candidate()
    names = make_package_names(candidate)
    requirements = (pkg2requirement(pkg) for pkg in set2sorted(names))

    with open(conf['requirements_filename'], "w") as f:
        f.write('\n'.join(requirements))
