from extract_details_highway_wise import Extract
import requests
import re
from collections import defaultdict
data = defaultdict(dict)
import concurrent.futures

def fetch_ids():
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
        }

        data = '{\'TollName\':\'\'}'

        response = requests.post('https://tis.nhai.gov.in/TollPlazaService.asmx/GetTollPlazaInfoGrid', headers=headers, data=data)

        toll_lists = re.findall('javascript:TollPlazaPopup\(\d+\)', response.text)
        toll_ids = [int(re.findall('\d+', id)[0]) for id in toll_lists]

        return toll_ids

def runetl(ids):
    etl_details = Extract(ids)
    etl_details.run()

def etl():
    ids = fetch_ids()
    print(ids)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(runetl, ids)

etl()
