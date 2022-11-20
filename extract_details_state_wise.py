import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import json

class Extract:

    def __init__(self, plaza_id) :
        self.plaza_id = plaza_id
        self.plaza_url = f'https://tis.nhai.gov.in/TollInformation.aspx?TollPlazaID={plaza_id}'
        self.soup = ''
        self.extract3()
    
    def extract1(self):
        response = requests.get(self.plaza_url)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        if self.soup.find(class_ = 'PA15'):
            return True
        return False
    
    def extract3(self):
        headers = {
        'Content-Type': 'application/json; charset=utf-8',
        }
        response = requests.post('https://tis.nhai.gov.in/TollPlazaService.asmx/GetTollPlazaInfoForMapOnPC', headers=headers)
        data = json.loads(response.text)
        self.data = data['d']
        
    def extract2(self, id):
        try:    
            self.id = id
            more_data = next((dic for dic in self.data if dic['TollPlazaID'] == id),None)
            
            if more_data['TollName'] is not None:
                plaza_name = more_data['TollName'] 
            else:
                plaza_name = 'ERROR'

            if more_data['latitude'] is not None:
                latitude = more_data['latitude'] 
            else:
                latitude = 'ERROR'
            
            if more_data['longitude'] is not None:
                longitude = more_data['longitude']
            else:
                longitude = 'ERROR'
            
            temp =  more_data['SearchLoc']
            if re.search(r'\d+', temp) is not None:
                highway_length = re.search(r'\d+', temp).group()
            else:
                highway_length = re.search(r'\d+', str(self.soup.find('div', attrs={'class':'PA15'}).find('p')).split('Km')[1].split(' - ')[0])
                if highway_length is None:
                    highway_length = 'NOT AVAILABLE'
                else:
                    highway_length = highway_length.group()
                
            print(highway_length)

            if more_data['ProjectType'] is not None:
                model = more_data['ProjectType']
            else:
                model = 'ERROR'

            state_name = self.soup.find('div', attrs={'class':'PA15'}).find('p').find_all('b')[1].text.split(' ')
            state_name = f'{state_name[-6]} {state_name[-5]}' if state_name[-6].strip() != 'in' else state_name[-5] 
            
            highway_name = self.soup.find('div', attrs={'class':'PA15'}).find('p').find_all('b')[1].text
            highway_name = re.search(r'\d+', highway_name)
            if highway_name is not None:
                highway_name = highway_name.group()
            else:
                highway_name = state_name+'_NO_NAME'
            highway_name = f'NH-{highway_name}' 
            
            table = pd.read_html(str(self.soup.find('table')))[0].dropna(how = 'all')
            table = table.dropna(how = 'all', axis = 1)
            if len(table) != 0:
                table = table.set_index('Type of vehicle')
                json_table = table.to_json(orient='index')
            else:
                json_table = {'DATA' : 'NOT AVAILABLE'}
            data = {highway_name : {'Highway Length' : highway_length, id : {'Plaza Name' : plaza_name, 'Latitude' : latitude, 'Longitude' : longitude,'Model' : model, 'Details' : json_table}}}
            return state_name, plaza_name, data    
        
        except Exception as e:
            print(id, more_data)