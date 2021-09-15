from replacemant import *
from plan_parser import *
from network import *

def get_time_plan():
    base_url = "http://www.ross-schulen.info/stundenplan/"
    class_name = "Kla1_BGIT21.htm"
    #class_name = "Kla1_PTA10.htm"
    plan_url = base_url + class_name

    website_user = "ross"
    website_pass = "hannover"

    plan_downloaded = requests.get(plan_url, auth=(website_user, website_pass)).text
    return plan_downloaded


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
    time_plan = get_all_class_names()
    #replacement_plan = get_replacement_plan()
    print(time_plan)
    #print(clean_table_index(get_table_index(replacement_plan)))

    # print(check_changes(time_plan, "plan.htm"))

