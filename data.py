from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset
from urllib import request
import numpy as np
import pandas as pd

def download_data():
    print('Downloading metadata...')
    try:
        Configuration.create(hdx_site='prod', user_agent='joaomarcos', hdx_read_only=True)
    except:
        ...
    dataset = Dataset.read_from_hdx('novel-coronavirus-2019-ncov-cases')

    resources = [r for r in dataset.get_resources() if 'iso3' in r['name']]
    for i in resources:
        print('Downloading', i['name'] + '...')
        request.urlretrieve(i['download_url'], i['name'])


def load_file(path):
    df = pd.read_csv(path, skiprows = [1])
    df = df.drop(columns = ['ISO 3166-1 Alpha 3-Codes', 'Region Code', 'Sub-region Code', 'Intermediate Region Code'])
    df['Province/State'] = df['Province/State'].fillna('')
    df['id'] = df['Province/State'] + '|' + df['Country/Region']
    df = df.set_index('id')
    return df

def load_data():
    df_cases = load_file('time_series_covid19_confirmed_global_iso3_regions.csv')
    df_deaths = load_file('time_series_covid19_deaths_global_iso3_regions.csv')
    df_recover = load_file('time_series_covid19_recovered_global_iso3_regions.csv')
    return df_cases, df_deaths, df_recover

class Province:
    def __init__(self, cases, deaths, recover):
        if cases is not None:
            s = cases
        elif deaths is not None:
            s = deaths
        else:
            s = recover

        self.name = s['Province/State']
        self.latitude = s['Lat']
        self.longitude = s['Long']
        self.country = s['Country/Region']
        self.continent = s['Region Name']
        self.sub_region = s['Sub-region Name']
        self.inter_region = s['Intermediate Region Name']
        
        self.cases = None
        self.daily_cases = None

        self.deaths = None
        self.daily_deaths = None

        self.recover = None
        self.daily_recover = None

        self.active = None
        self.daily_active = None

        if cases is not None:
            cases = cases.drop(['Province/State', 'Lat', 'Long', 'Country/Region', 'Region Name', 'Sub-region Name', 'Intermediate Region Name'])
            self.cases = cases.to_numpy()
            dc = self.cases.copy()
            self.daily_cases = np.array([dc[i] - dc[i-1] for i in range(1,len(dc))])
        if deaths is not None:
            deaths = deaths.drop(['Province/State', 'Lat', 'Long', 'Country/Region', 'Region Name', 'Sub-region Name', 'Intermediate Region Name'])
            self.deaths = deaths.to_numpy()
            dd = self.deaths.copy()
            self.daily_deaths = np.array([dd[i] - dd[i-1] for i in range(1,len(dd))])
        if recover is not None:
            recover = recover.drop(['Province/State', 'Lat', 'Long', 'Country/Region', 'Region Name', 'Sub-region Name', 'Intermediate Region Name'])
            self.recover = recover.to_numpy()
            dr = self.recover.copy()
            self.daily_recover = np.array([dr[i] - dr[i-1] for i in range(1,len(dr))])

        if cases is not None and deaths is not None and recover is not None:
            self.active = self.cases - self.deaths - self.recover
            self.daily_active = self.daily_cases - self.daily_deaths - self.daily_recover

class Country:
    def __init__(self, name):
        self.provinces = []

        self.name = name

    def add(self, province):
        self.provinces.append(province)

    def finish(self):
        self.latitude = np.mean([p.latitude for p in self.provinces])
        self.latitude = np.mean([p.longitude for p in self.provinces])

        self.continent = self.provinces[0].continent
        self.sub_region = self.provinces[0].sub_region
        self.inter_region = self.provinces[0].inter_region

        self.cases = np.sum(np.array([p.cases for p in self.provinces if p.cases is not None]), axis=0)
        self.daily_cases = np.sum(np.array([p.daily_cases for p in self.provinces if p.daily_cases is not None]), axis = 0)
        
        self.deaths = np.sum(np.array([p.deaths for p in self.provinces if p.deaths is not None]), axis = 0)
        self.daily_deaths = np.sum(np.array([p.daily_deaths for p in self.provinces if p.daily_deaths is not None]), axis = 0)

        self.recover = np.sum(np.array([p.recover for p in self.provinces if p.recover is not None]), axis = 0)
        self.daily_recover = np.sum(np.array([p.daily_recover for p in self.provinces if p.daily_recover is not None]), axis = 0)
        
        self.active = np.sum(np.array([p.active for p in self.provinces if p.active is not None]), axis = 0)
        self.daily_active = np.sum(np.array([p.daily_active for p in self.provinces if p.daily_active is not None]), axis = 0)

def process_data(df_cases, df_deaths, df_recover):
    Provinces = {}
    Countries = {}

    ids = [i for i in list(df_cases.index.unique()) if i in list(df_deaths.index.unique()) and i in list(df_recover.index.unique())]
    ids = set(ids)
    
    for id in ids:
        cases = None
        deaths = None
        recover = None

        if id in df_cases.index:
            cases = df_cases.loc[id]
        if id in df_deaths.index:
            deaths = df_deaths.loc[id]
        if id in df_recover.index:
            recover = df_recover.loc[id]

        p = Province(cases, deaths, recover)
        Provinces[id] = p
        
        if p.country in Countries:
            Countries[p.country].add(p)
        else:
            Countries[p.country] = Country(p.country)
            Countries[p.country].add(p)

    for c in Countries:
        Countries[c].finish()
    
    return Provinces, Countries
        
        
