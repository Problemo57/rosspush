from plan_parser import *
from database import *
from network import *


def check_changes(plan, save_location):

    try:
        with open(save_location, "r") as r:
            # For some reason, when the plan gets writen to the disk and read again,
            # the line endings will change from \r\n to \n\n.
            saved_plan = r.read().replace("\n\n", "\r\n")

        if plan == saved_plan:
            return False

    except FileNotFoundError:
        pass

    with open(save_location, "w") as w:
        w.write(plan)

    return True


if __name__ == "__main__":
    db = Database("user.db")
    if db.isEmpty():
        class_names = get_all_class_names()
        db.reset_database(class_names)
    db.close()
