import requests


def _fetch_website(url):
    website_user = "ross"
    website_pass = "hannover"

    return requests.get(url, auth=(website_user, website_pass)).text


def _fetch_names(url):
    class_names_html = _fetch_website(url)

    class_names_filtered = [i.split("</A>")[0] for i in class_names_html.split('<A HREF="')][1:-1]
    class_names = {i.split('">')[1]: i.split('">')[0] for i in class_names_filtered}

    return class_names


def get_all_class_names():
    url = "http://www.ross-schulen.info/stundenplan/Kla1.htm"
    class_names = _fetch_names(url)

    return class_names


def get_all_room_names():
    url = "http://www.ross-schulen.info/stundenplan/Rau1.htm"
    room_names = _fetch_names(url)

    return room_names


def get_all_teacher_names():
    url = "http://www.ross-schulen.info/stundenplan/Leh1.htm"
    teacher_names = _fetch_names(url)

    return teacher_names


def get_time_plan(class_name):
    base_url = "http://www.ross-schulen.info/stundenplan/"
    plan_url = base_url + class_name

    return _fetch_website(plan_url)


def get_room_plan(room_name):
    base_url = "http://www.ross-schulen.info/stundenplan/"
    plan_url = base_url + room_name

    return _fetch_website(plan_url)


def get_teacher_plan(teacher_name):
    base_url = "http://www.ross-schulen.info/stundenplan/"
    plan_url = base_url + teacher_name

    return _fetch_website(plan_url)
