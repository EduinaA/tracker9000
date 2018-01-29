import requests
from bs4 import BeautifulSoup

def get_last_rows(response_html, num_rows=4):
    rows = []
    soup = BeautifulSoup(response_html, 'html.parser')
    tr_list = soup.find_all('tr')
    for tr in tr_list:
        # print('tr contents', tr)
        td_list = tr.find_all('td')
        if td_list == []:
            continue
        if num_rows <= 0:
            break
        row = [td.get_text() for td in td_list]
        rows.append(row)
        num_rows -= 1
    return rows

def get_last_row(response_html):
    rows = get_last_rows(response_html, num_rows=1)
    return rows[0]

# /track AA000000000AA


def show_track(tracking_number):
    form_params = {
        'txt_barcode': tracking_number,
        'hBarCodes': tracking_number,
        'btn_track': 'Gjurmo/Submit',
        #'__EVENTARGUMENT': '',
        #'__EVENTTARGET': '',
        '__VIEWSTATE': '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',
        '__EVENTVALIDATION': '/wEdAAVq1u8xZDwT0CkmVH0TYDLts/foFj56M4JV9YiCGX9Oya9U1URXbQkTl8PXilbzpbKyuB7QXXlyP7hBJbH/uNLRemgLggfoCsFv2TROt6obiSk5oiOy8uVqek1f9Q9uepTiyD8Dpn7KARBvEgFcPp05'
    }
    response = requests.post('http://79.106.191.16/tracking.aspx', data=form_params)
    row = get_last_row(response.content)
    return row

def main():
    last_row = show_track('RU831778273GB')
    assert len(last_row) == 4

if __name__ == '__main__':
    main()