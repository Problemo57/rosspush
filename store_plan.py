import requests
import time


def get_plan():
    base_url = "http://www.ross-schulen.info/stundenplan/"
    class_name = "Kla1_BGIT21.htm"
    plan_url = base_url + class_name

    website_user = "ross"
    website_pass = "hannover"

    plan_downloaded = requests.get(plan_url, auth=(website_user, website_pass)).text
    return plan_downloaded


if __name__ == "__main__":
    plan = get_plan()

    try:
        with open("plan.htm", "r") as r:
            p = r.read()
        with open("plan.htm", "w") as w:
            w.write(plan)
        with open("plan.htm", "r") as r:
            p2 = r.read()


        if p == p2:
            print("Same")
            exit()

    except FileNotFoundError:
        pass

    with open("plan.htm", "w") as w:
        w.write(plan)

    with open(str(time.time()), "w") as w:
        w.write(plan)
