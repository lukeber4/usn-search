# usn-search
usn-search is a tool to import USN (Ubuntu Security Notices) database dump into a MongoDB to facilitate search and processing of CVEs and its packages.

Given (.deb) packages, you can check if there are known vulnerabilities that affects them.

*Dump last updated: 07/07/2018*

# Requirements
   * MongoDB (2.2 or above)
   * Python3
   * Pip3:
     * PyMongo
     * natsort
     * lxml

# Installation
1. Git clone the repo:

    ```
    $ git clone https://github.com/lukeber4/usn-search/ && cd usn-search/
    ```    
    
2. First we install the requirements:

    ```
    $ sudo pip3 install -r requirements.txt
    ```

3. We extract cves.out.gz:

    ```
    $ gzip -d cves.out.gz
    ```
    
4. MongoDB installation: you can get the distribution packages here: https://docs.mongodb.com/manual/installation/.
If Ubuntu, here is the guide: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
5. Once Mongo is installed and running, we populate the MongoDB with Ubuntu's CVEs dump (should take 4-5 minutes aprox):

    ```
    $ python3 insert_mongo.py
    ```
6. We are ready to go!

# Usage
```
$ python3 search.py -h
usage: search.py [-h] [-p PACKAGE] [-v VERSION] [-o OS] [-c CVE] [-a]

USN Search.

optional arguments:
  -h, --help            show this help message and exit
  -p PACKAGE, --package PACKAGE
                        package --> e.g: -p php5
  -v VERSION, --version VERSION
                        package version (optional) --> e.g: -p php5 -v 5.2.1
  -o OS, --os OS        OS or upstream --> e.g: -o 14.04
  -c CVE, --cve CVE     Specific CVE information --> -c CVE-2015-1258
  -a, --all             Show unclassified CVEs (no fix or not Ubuntu related)
```

# Examples
1. Listing all CVEs:

    ```
    $ python3 search.py | wc -l
    122872
    ```
    You can also list unclassified CVEs (with no fix version or not Ubuntu related):
    
    ```
    $ python3 search.py -a | wc -l
    960894
    ```
    Example:
    ```
    $ python3 search.py | head
    CVE-2014-4207: [Medium] Package mysql-5.5, fix version: 5.5.38-0ubuntu0.12.04.1 [Ubuntu 12.04 Lts (Precise Pangolin)] (http://people.canonical.com/~ubuntu-security/cve/2014/CVE-2014-4207.html)
    CVE-2014-4207: [Medium] Package mariadb-5.5, fix version: 5.5.38 [Upstream] (http://people.canonical.com/~ubuntu-security/cve/2014/CVE-2014-4207.html)
    CVE-2007-1536: [Untriaged] Package file, fix version: 4.21 [Upstream] (http://people.canonical.com/~ubuntu-security/cve/2007/CVE-2007-1536.html)
    CVE-2012-2772: [Low] Package libav, fix version: 4:0.8.4-0ubuntu0.12.04.1 [Ubuntu 12.04 Lts (Precise Pangolin)] (http://people.canonical.com/~ubuntu-security/cve/2012/CVE-2012-2772.html)
    CVE-2012-3991: [High] Package firefox, fix version: 16.0 [Upstream] (http://people.canonical.com/~ubuntu-security/cve/2012/CVE-2012-3991.html)
    [...]
    ```
2. You can also search for a specific package:

    ```
    $ python3 search.py -p redis
    CVE-2013-0180: [Low] Package redis, fix version: 2:2.6.7-1 [Upstream] (http://people.canonical.com/~ubuntu-security/cve/2013/CVE-2013-0180.html)
    CVE-2015-4335: [Medium] Package redis, fix version: 2:3.0.2-1 [Upstream] (http://people.canonical.com/~ubuntu-security/cve/2015/CVE-2015-4335.html)
    CVE-2013-7458: [Medium] Package redis, fix version: 2:3.2.1-4 [Upstream] (http://people.canonical.com/~ubuntu-security/cve/2013/CVE-2013-7458.html)
    CVE-2016-8339: [Medium] Package redis, fix version: 3:3.2.4-1 [Upstream] (http://people.canonical.com/~ubuntu-security/cve/2016/CVE-2016-8339.html)

    ```
3. If you use X version, you can check if there are vulnerabilities for a newer version (making yours vulnerable):

    ```
    $ python3 search.py -p c-ares -v 1.10.0
    CVE-2016-5180: [Medium] Package c-ares, fix version: 1.10.0-2ubuntu0.1 [Ubuntu 14.04 Lts (Trusty Tahr)] (http://people.canonical.com/~ubuntu-security/cve/2016/CVE-2016-5180.html)
    CVE-2016-5180: [Medium] Package c-ares, fix version: 1.10.0-3ubuntu0.1 [Ubuntu 16.04 Lts (Xenial Xerus)] (http://people.canonical.com/~ubuntu-security/cve/2016/CVE-2016-5180.html)
    CVE-2016-5180: [Medium] Package c-ares, fix version: 1.11.0-1ubuntu0.1 [Ubuntu 16.10 (Yakkety Yak)] (http://people.canonical.com/~ubuntu-security/cve/2016/CVE-2016-5180.html)
    CVE-2016-5180: [Medium] Package c-ares, fix version: 1.12.0 [Upstream] (http://people.canonical.com/~ubuntu-security/cve/2016/CVE-2016-5180.html)
    ```
4. You can limit your search for a specific OS version too:

    ```
    $ python3 search.py -p nginx -v 1.4.6-1ubuntu3.4 -o 14.04
    CVE-2016-4450: [Medium] Package nginx, fix version: 1.4.6-1ubuntu3.5 [Ubuntu 14.04 Lts (Trusty Tahr)] (http://people.canonical.com/~ubuntu-security/cve/2016/CVE-2016-4450.html)
    CVE-2016-1247: [Medium] Package nginx, fix version: 1.4.6-1ubuntu3.6 [Ubuntu 14.04 Lts (Trusty Tahr)] (http://people.canonical.com/~ubuntu-security/cve/2016/CVE-2016-1247.html)
    ```
    If you also want to know if there are CVEs for a package without fix versions, try -a:
    
    ```
    $ python3 search.py -p nginx -v 1.4.6-1ubuntu3.4 -o 14.04 -a
    CVE-2013-4547: [Medium] Package nginx is not affected [Ubuntu 14.04 Lts (Trusty Tahr)]
    CVE-2016-4450: [Medium] Package nginx, fix version: 1.4.6-1ubuntu3.5 [Ubuntu 14.04 Lts (Trusty Tahr)] (http://people.canonical.com/~ubuntu-security/cve/2016/CVE-2016-4450.html)
    CVE-2014-0088: [Medium] Package nginx is not affected [Ubuntu 14.04 Lts (Trusty Tahr)]
    CVE-2013-0337: [Low] Package nginx doesn't have a released fix version [Ubuntu 14.04 Lts (Trusty Tahr)]
    CVE-2011-4968: [Low] Package nginx is not affected [Ubuntu 14.04 Lts (Trusty Tahr)]
    [...]
    ```

5. Information about certain CVE:

    ```
    $ python3 search.py -c CVE-2013-7341
    CVE-2013-7341: [Medium] Package moodle, fix version: 2.5.5 [Upstream] (http://people.canonical.com/~ubuntu-security/cve/2013/CVE-2013-7341.html)
    CVE-2013-7341: [Medium] Package moodle doesn't have a released fix version [Ubuntu 14.04 Lts (Trusty Tahr)]
    CVE-2013-7341: [Medium] Package moodle is not affected [Ubuntu Touch 15.04]
    CVE-2013-7341: [Medium] Package moodle is not affected [Ubuntu Core 15.04]
    ```
