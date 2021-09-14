import requests


def get_replacement_plan():
    url = "http://www.ross-schulen.info/vertretungsplan/"
    website_user = "ross"
    website_pass = "hannover"

    plan_downloaded = requests.get(url, auth=(website_user, website_pass)).text
    return plan_downloaded


def get_table_index(html):
    table = html.split("<table cellpadding=4 cellspacing=4 border=0>")[1].split("</table>")[0]
    return table.split("</tR>")[1:-1]


def clean_table_index(index):
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
