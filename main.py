from plan_parser import *
from database import *
from network import *
from server_api import *
from notifications import *


def init_database():
    db = Database("user.db")
    if db.isEmpty():
        class_names = get_all_class_names()
        db.reset_database(class_names)
    db.close()


def save_time_plan(time_plan, save_location):
    if not os.path.exists("www"):
        os.mkdir("www")

    save_location = save_location.replace("/", "%F3")
    fp = open(f"www/{save_location}.json", "w")
    json.dump(time_plan, fp)
    fp.close()


def load_time_plan(save_location):
    save_location = save_location.replace("/", "%F3")
    fp = open(f"www/{save_location}.json", "r")
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
    return True


def check_all_files_for_changes():
    class_names = get_all_class_names()
    changed_files = []

    for class_name, class_url in class_names.items():

        time_plan = parse_time_plan(get_time_plan(class_url))
        changed = check_changes(time_plan, class_url)

        if changed:
            changed_files += [class_name]

    return changed_files


def send_notification_to_change_classes(change_classes):
    for class_name in change_classes:
        db = Database("user.db")
        device_token = db.read_entrys(class_name)
        db.close()

        notification = {
            'title': f'Der Stundenplan der Klasse {class_name} hat sich geändert.'
            # 'body': 'New Message'
        }

        notifiy_class(device_token, notification)


if __name__ == "__main__":
    init_database()

    change_files = check_all_files_for_changes()
    print("Found change Time Plans:", change_files)
    send_notification_to_change_classes(change_files)

    # updatePlans()
    #port = 18573
    #main(port)


