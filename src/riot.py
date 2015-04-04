import requests

class Riot:
    api_key = None
    region = None
    valid_regions = None

    summoner_version = 'v1.4'
    
    base_api_url = 'https://{0}.api.pvp.net'
    base_summoner_suffix = '/api/lol/{0}/{1}/summoner'
    base_summoner_url = None

    MAX_ID_LIST = 40

    def check_region(self):
        if not self.region or self.region not in self.valid_regions:
            raise Exception('You need to provide a valid region for this call.')

    def init_valid_regions(self):
        self.valid_regions = ['br', 'eune', 'euw', 'kr', 'lan', \
                              'las', 'na', 'oce', 'ru', 'tr' \
                             ]

    def init_base_url(self):
        self.check_region()
        self.base_api_url = self.base_api_url.format(self.region)

    def init_summoner_url(self):
        if self.base_summoner_url:
            return True

        self.check_region()
        base_summoner_suffix = self.base_summoner_suffix.format(self.region \
                                                               ,self.summoner_version \
                                                               )
        self.base_summoner_url = self.base_api_url + base_summoner_suffix

    def get_api_key_query_string(self):
        return '?api_key={0}'.format(self.api_key)

    def set_region(self, region):
        self.region = self.standardize_name(region) 

    def __init__(self, api_key, region = None):
        self.api_key = api_key
        self.set_region(region)
        self.init_valid_regions()
        self.init_base_url()

    def standardize_name(self, name):
        if not name or not isinstance(name, str):
            return False

        return name.replace(' ', '').lower()

    def parse_name_list(self, names):
        if not names:
            return False

        names = str(names)

        if isinstance(names, list):
            names = ','.join(names)
        
        return self.standardize_name(names)

    def parse_id_list(self, ids):
        if not ids:
            return False

        exceeded_exception = Exception('You are querying the server for more than ' \
                               + str(self.MAX_ID_LIST) + 'names.')

        if isinstance(ids, list):
            if len(ids) > self.MAX_ID_LIST:
                raise exceeded_exception

            ids = [str(_id) for _id in ids]

            return ','.join(ids)
        elif isinstance(ids, str):
            if ids.count(',') > (self.MAX_ID_LIST - 1):
                raise exceeded_exception

            return ids.replace(' ', '')

    def get_summoner_by_name(self, names):
        self.init_summoner_url()
        names = self.parse_name_list(names)

        if not names:
            raise Exception('Riot: No name provided.')

        url = self.base_summoner_url + '/by-name'
        url += '/' + names + self.get_api_key_query_string()
        
        return requests.get(url).text

    def get_summoner_by_id(self, ids):
        self.init_summoner_url()
        ids = self.parse_id_list(ids)

        if not ids: 
            raise Exception('Id list provided not valid.')

        url = self.base_summoner_url
        url += '/' + ids + self.get_api_key_query_string()

        return requests.get(url).text
