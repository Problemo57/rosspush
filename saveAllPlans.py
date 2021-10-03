from network import *
from plan_parser import *
import os
import json
import time


def save_time_plan(time_plan, save_location):
    if not os.path.exists("saved"):
        os.mkdir("saved")

    save_location = save_location.replace("/", "%F3")
    fp = open(f"saved/{save_location}.json", "w")
    json.dump(time_plan, fp)
    fp.close()


def load_time_plan(save_location):
    save_location = save_location.replace("/", "%F3")
    fp = open(f"saved/{save_location}.json", "r")
    time_plan = json.load(fp)
    fp.close()
    return time_plan


def check_changes(time_plan, class_url):
    try:
        old_time_plan = load_time_plan(class_url)
        if time_plan == old_time_plan:
            return False

    except FileNotFoundError:
        pass

    save_time_plan(time_plan, class_url)
    save_time_plan(time_plan, f"{class_url}-{time.time()}")
    return True


def check_all_files_for_changes():
    class_names = get_all_class_names()
    room_names = get_all_room_names()
    teacher_names = get_all_teacher_names()

    class_names.update(room_names)
    class_names.update(teacher_names)
    save_time_plan(class_names, "names")
    changed_files = []

    for class_name, class_url in class_names.items():

        time_plan = get_time_plan(class_url)
        changed = check_changes(time_plan, class_url)

        if changed:
            changed_files += [class_name]

    return changed_files


if __name__ == "__main__":
    print(check_all_files_for_changes())
