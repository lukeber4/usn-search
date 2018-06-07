from pymongo import MongoClient


def store_cve(db, package, os, version, cve, status, priority):
    db.cve_ubuntu.insert_one(
        {
            "package": package.lower(),
            "os": os.lower(),
            "version": version.lower(),
            "cve": cve.lower(),
            "status": status.lower(),
            "priority": priority.lower(),
        })


def main():
    client = MongoClient()
    db = client.cve_ubuntu
    with open("cves.out") as file:
        for line in file:
            line = line.rstrip('\n')
            package = line.split('"')[1]
            os = line.split('"')[3]
            version = line.split('"')[5]
            cve = line.split('"')[7]
            status = line.split('"')[9]
            priority = line.split('"')[11]
            store_cve(db, package, os, version, cve, status, priority)


if __name__ == "__main__":
    main()
