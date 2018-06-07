import argparse
import re
from pymongo import MongoClient
from natsort import natsorted


def create_link(cve):
    year = cve.split("-")[1]
    url = "http://people.canonical.com/~ubuntu-security/cve/{}/{}.html".format(year, cve.upper())
    return url


def search(data):
    client = MongoClient()
    db = client.cve_ubuntu
    return db.cve_ubuntu.find(data)


def get_args():
    parser = argparse.ArgumentParser(description='USN Search.')
    parser.add_argument('-p', '--package', help='package --> e.g: -p php5')
    parser.add_argument('-v', '--version', help='package version (optional) --> e.g: -p php5 -v 5.2.1')
    parser.add_argument('-o', '--os', help='OS or upstream -->  e.g: -o 14.04')
    parser.add_argument('-c', '--cve', help='Specific CVE information --> -c CVE-2015-1258')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Show unclassified CVEs (no fix or not Ubuntu related)')
    args = parser.parse_args()
    package = args.package
    version = args.version
    os = args.os
    cve = args.cve
    show_all = args.all
    return package, version, os, cve, show_all


def version_is_vulnerable(version, cve_version):
    l = [version, cve_version]
    if natsorted(l).index(version) < natsorted(l).index(cve_version):
        return True
    return False


def format_data(package, os, cve, show_all):
    data = {}
    if package:
        data['package'] = package
    if os:
        data['os'] = re.compile('.*{}.*'.format(os))
    if cve:
        data['cve'] = cve.lower()
    if len(data) == 0 and not show_all:  # no arguments received
        data['package'] = {"$ne": ""}
    return data


def print_results(result):
    if result['package']:
        if result['version'] and result['status'] == 'released':
            link = create_link(result['cve'])
            print("{}: [{}] Package {}, fix version: {} [{}] ({})".format(result['cve'].upper(), result['priority'].title(), result['package'],
                                                                     result['version'], result['os'].title(),
                                                                     link))
        elif result['status'] == 'needed':
            print("{}: [{}] Package {} doesn't have a released fix version [{}]".format(result['cve'].upper(),
                                                                                        result['priority'].title(),
                                                                                        result['package'],
                                                                                        result['os'].title()))
        else:
            print("{}: [{}] Package {} is not affected [{}]".format(result['cve'].upper(),
                                                                                        result['priority'].title(),
                                                                                        result['package'],
                                                                                        result['os'].title()))
    else:
        print("{}: Does not apply to software found in Ubuntu".format(result['cve'].upper()))


def get_results():
    package, version, os, cve, show_all = get_args()
    data = format_data(package, os, cve, show_all)
    results = search(data)
    try:
        for result in results:
            if result['package']:
                if result['version'] and result['status'] == 'released':
                    if version:  # if user provided a version
                        if version_is_vulnerable(version, result['version']):  # we check if version is vulnerable
                            print_results(result)
                    else:
                        print_results(result)
                else:
                    if cve or show_all:
                        print_results(result)
            else:
                print_results(result)
    except:
        print("Interrupted.")


def main():
    get_results()


if __name__ == "__main__":
    main()
