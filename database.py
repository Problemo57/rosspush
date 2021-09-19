import json
import os.path
from time import sleep


def wait_until_file_is_free(filename):
    while os.path.isfile(f"{filename}.lock"):
        sleep(1)

    print("Database is free")


def block_file(filename):
    with open(f"{filename}.lock", "w") as _:
        pass


class Database:
    db = {}

    def __init__(self, filename):
        wait_until_file_is_free(filename)
        block_file(filename)
        self.filename = filename

        # If file exists read it, if not make it
        mode = "r" if os.path.isfile(filename) else "w"

        with open(filename, mode) as r:
            if mode == "r":
                filedata = r.read()
                if not filedata:
                    filedata = "{}"

                self.db = json.loads(filedata)

            else:
                self.db = {}

    def reset_database(self, class_names):
        self.db = {}

        if type(class_names) == dict:
            for i, _ in class_names.items():
                self.db[i] = {}

        elif type(class_names) == list:
            for i in class_names:
                self.db[i] = {}

        else:
            print("ERROR: class_names type invalid! Only list and dict")

    def read_entry(self, class_name, entry_name):
        return self.db[class_name][entry_name]

    def read_entrys(self, class_name):
        return self.db[class_name]

    def add_entry(self, class_name, entry_name, entry_data=""):
        self.db[class_name][entry_name] = entry_data

    def delete_entry(self, class_name, entry_name):
        self.db[class_name].pop(entry_name)

    def close(self):

        fp = open(self.filename, "w")
        json.dump(self.db, fp)
        fp.close()

        os.remove(f"{self.filename}.lock")


def main():
    db = Database("user.db")
    db.reset_database(["1", "2", "5"])
    print(db.db)
    db.add_entry("1", "i", "fdweweffer")
    print(db.db)
    db.delete_entry("1", "i")
    print(db.db)
    db.close()
