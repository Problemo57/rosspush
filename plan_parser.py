from abc import ABC
from html.parser import HTMLParser
import json


class _PlanParser(HTMLParser, ABC):

    table_tag_level = 0
    time_table_table_found = 0  # 0: NO, 1: Found, 2: Write to time_plan

    # Makes a two dimensional Dict. 10*12
    time_plan = {i/2+0.5: {x: {"same_as_before": False, "nothing": False, "free": False} for x in range(1, 13)} for i in range(1, 11)}

    # The first tr Tag is not a school hour
    time_hour_count = -1

    # Increments per td by 0.5 and hour index starts at 1
    time_day_count = 0.5

    # Used for knowing what info the "handle_data" function gets
    time_day_hour_info_state = 0

    # Used first to find the right table und second in handle_data to find free hours
    encounters = 0

    def __init__(self, plan_typ):
        super().__init__()
        self.plan_typ = plan_typ

        self.table_tag_level = 0
        self.time_table_table_found = 0  # 0: NO, 1: Found, 2: Write to time_plan

        # Makes a two dimensional Dict. 10*12
        self.time_plan = {i/2+0.5: {x: {"same_as_before": False, "nothing": False, "free": False} for x in range(1, 13)} for i in range(1, 11)}

        # The first tr Tag is not a school hour
        self.time_hour_count = -1

        # Increments per td by 0.5 and hour index starts at 1
        self.time_day_count = 0.5

        # Used for knowing what info the "handle_data" function gets
        self.time_day_hour_info_state = 0

        # Used first to find the right table und second in handle_data to find free hours
        self.encounters = 0

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.table_tag_level += 1

            if not self.time_table_table_found:
                self.encounters += 1

                if self.encounters == 2:
                    self.time_table_table_found = 1
                    self.table_tag_level = 1

        if not self.table_tag_level == 1 or not self.time_table_table_found:
            return

        if tag == "tr":
            self.time_hour_count += 1
            self.time_day_count = 0.5

            if self.time_hour_count <= 0:
                return

            self.time_table_table_found = 2
            # print("Hour: ", self.time_hour_count)

        elif tag == "td":
            if "colspan" not in [x[0] for x in attrs] or self.time_table_table_found != 2:
                return

            # handle_data needs it
            self.time_day_hour_info_state = 0
            self.encounters = 0

            # Shortcut
            sab = "same_as_before"

            # Normal Day increment
            self.time_day_count += 0.5

            # Skipping days where the lesson from the hour before is still ongoing or where no lessons are
            while self.time_day_count < 6 and self.time_plan[self.time_day_count][self.time_hour_count][sab]\
                    or self.time_plan[self.time_day_count][self.time_hour_count]["nothing"]:
                self.time_day_count += 0.5

            # No school on saturday
            if self.time_day_count >= 6:
                return

            # If only one hour at a time, set nothing on the .5 time
            one_hour = [c[1] for c in attrs if c[0] == "colspan"][0] == "6"
            if one_hour:
                self.time_plan[self.time_day_count + 0.5][self.time_hour_count]["nothing"] = True

            # Marking the next hours defined in "rowspan" as same_as_before(sab)
            # print("Day: ", self.time_day_count, "Hour: ", self.time_hour_count)
            rowspan = [int(r[1]) for r in attrs if r[0] == "rowspan"]
            if rowspan:
                for i in range(rowspan[0] - 1):
                    self.time_plan[self.time_day_count][self.time_hour_count+i+1][sab] = True

                    if one_hour:
                        self.time_plan[self.time_day_count+0.5][self.time_hour_count+i+1]["nothing"] = True

            # print("Day: ", self.time_day_count, attrs)

    def handle_endtag(self, tag):
        if tag == "table":
            self.table_tag_level -= 1

            if self.table_tag_level == 0:
                self.time_table_table_found = False

        elif tag == "td":
            if not self.time_table_table_found or self.time_day_count == 0.5:
                return

            # If only one encounter means there is a free hour
            if self.encounters <= 1 and self.table_tag_level == 1:
                self.time_plan[self.time_day_count][self.time_hour_count]["free"] = True

    def handle_data(self, data):
        # Remove "\n", "\r" and " " from start and end of string
        data = data.strip()
        if self.time_day_count == 0.5 or not self.time_table_table_found:
            return

        if not data:
            self.encounters += 1
            return

        # 0 -> 1 -> 2 -> 0
        self.time_day_hour_info_state = (self.time_day_hour_info_state + 1) % 3
        info_name = ["lesson", "teacher", "room"][self.time_day_hour_info_state]

        self.time_plan[self.time_day_count][self.time_hour_count][info_name] = data


def _clean_half_days(time_plan):
    for d in range(1, len(time_plan)//2 + 1):
        for h in range(1, len(time_plan[d+0.5]) + 1):

            # Remove nothing from .0 items
            time_plan[d][h].pop("nothing")

            if time_plan[d + 0.5][h]["nothing"]:
                continue

            # Remove nothing from .5 items
            time_plan[d + 0.5][h].pop("nothing")

            # Add time_plan from .5 to .0
            time_plan[d][h]["alternative_plan"] = time_plan[d + 0.5][h]

        time_plan.pop(d + 0.5)


def _clean_free_hours(parsing_data):
    for d in range(1, len(parsing_data) + 1):
        before_true = False

        for h in range(1, len(parsing_data[d]) + 1):

            if before_true and parsing_data[d][h]["same_as_before"]:
                parsing_data[d][h]["free"] = True

            before_true = parsing_data[d][h]["free"]


def _remove_float(parsing_data):
    return {int(k): v for k, v in parsing_data.items()}


def _clean_parsing_output(parsing_data):
    _clean_half_days(parsing_data)
    _clean_free_hours(parsing_data)
    parsing_data = _remove_float(parsing_data)

    # Changes the int keys to string
    return json.loads(json.dumps(parsing_data))


def _get_table_index(html):
    table = html.split("<table cellpadding=4 cellspacing=4 border=0>")[1].split("</table>")[0]
    return table.split("</tR>")[1:-1]


def _clean_table_index(index):
    # nobr musst be done before <tr><td valign=middle align=right></td><td valign=top></td>
    useless_html = [
        "<nobr>", "</nobr>",
        "<tr><td valign=middle align=right></td><td valign=top></td>",
        "<b>", "</b>", "<br>",
        "<font color='#666666'>", "</font>",
        "</td>", "</tD>",
        " valign=top"
    ]

    for i in range(len(index)):

        for r in useless_html:
            index[i] = index[i].replace(r, "")

        index[i] = index[i].split("<td>")[1:]

    return index


def parse_time_plan(time_plan):
    parser = _PlanParser("time_plan")
    parser.feed(time_plan)
    parsing_data = parser.time_plan

    parsing_data = _clean_parsing_output(parsing_data)
    return parsing_data


def parse_room_plan(room_plan):
    parser = _PlanParser("room_plan")
    parser.feed(room_plan)
    parsing_data = parser.time_plan

    parsing_data = _clean_parsing_output(parsing_data)
    return parsing_data


def parse_replacement_plan(replacement_plan):
    table_index = _get_table_index(replacement_plan)
    return _clean_table_index(table_index)
