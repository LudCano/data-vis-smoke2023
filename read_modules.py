

import pandas as pd
import matplotlib.dates as mdates
import numpy as np

tab = pd.read_csv('data.csv')
varss = tab.variable.unique()
places = tab.place.unique()
origin = tab.origin.unique()


class goes:
    def __init__(self, pth, place, units):
        d = pd.read_csv(pth, skiprows=6)

        #getting metadata just in case
        f = open(pth, 'r')
        m = f.readlines()
        self.metadata = '  '.join(m[:6])

        #working on reading the data and if necessary filter the data
        d.time_start = pd.to_datetime(d.time_start)
        d = d.sort_values('time_start')
        d.reset_index(inplace=True)
        self.times = d.time_start.to_list()
        place = " " + place
        self.values = np.array(d[place])
        self.datenum = mdates.date2num(d.time_start)
        d = d.loc[:, ['time_start', place]]
        d['datenum'] = mdates.date2num(d.time_start)
        self.df = d
        self.path = pth
        self.units = units
    def showmetadata(self):
        #getting metadata just in case
        f = open(self.path, 'r')
        m = f.readlines()
        for i in m[:6]:
            print(i)


class cimel:
    def __init__(self, pth, unidad, units):
        
        d = pd.read_csv(pth, skiprows=4)

        #getting metadata just in case
        f = open(pth, 'r')
        m = f.readlines()
        self.metadata = '  '.join(m[:4])

        #working on reading the data and if necessary filter the data
        d.date_local = pd.to_datetime(d.date_local)
        d.reset_index(inplace=True)
        if not unidad==None:
            #d = d.loc[:, ['time_start', ' time_end', place]]
            d = d.loc[:, ['date_local', unidad]]
        d['numdate'] = mdates.date2num(d.date_local)
        self.times = d.date_local.to_list()
        self.datenum = np.array(d.numdate)
        self.df = d
        self.values = np.array(d[unidad])
        self.path = pth
        self.units = units
    def showmetadata(self):
        #getting metadata just in case
        f = open(self.path, 'r')
        m = f.readlines()
        for i in m[:4]:
            print(i)


def read(origin,place,variable):
    tab = pd.read_csv('data.csv')
    tab2 = tab[(tab.origin == origin) & (tab.place == place) & (tab.variable == variable)]
    if len(tab2) != 1:
        print("Error, bad combination, returning None")
        print("Your options were:")
        print("Origin: ", origin)
        print("Place:", place)
        print("Variable", variable)
        c = None
    else:
        if origin == "GOES":
            c = goes(tab2.path.to_list()[0], place, tab2.units.to_list()[0])
        elif origin == 'CIMEL':
            c = cimel(tab2.path.to_list()[0], variable, tab2.units.to_list()[0])

    return c

### -------------------------
### FUNCTIONS: DEPRECATED
### -------------------------
'''
def read_goes(pth, place=None):
    """Reads a GOES stations data file (.csv)
    Doesn't work for vertical profiles, there's another function for that.

    Args:
        pth (str): Route to the datafile
        place (str, optional): Place to get the data. Defaults to None.

    Returns:
        d: Dataframe of the data
        m: Metadata that is the first 6 rows
    """

    d = pd.read_csv(pth, skiprows=6)

    #getting metadata just in case
    f = open(pth, 'r')
    m = f.readlines()
    m = '  '.join(m[:6])

    #working on reading the data and if necessary filter the data
    d.time_start = pd.to_datetime(d.time_start)
    d = d.sort_values('time_start')
    d.reset_index(inplace=True)
    if not place==None:
        place = " " + place
        #d = d.loc[:, ['time_start', ' time_end', place]]
        d = d.loc[:, ['time_start', place]]
    d['numdate'] = mdates.date2num(d.time_start)

    return d, m


def read_cimel(pth, unidad=None):
    """Reads a CIMEL file data

    Args:
        pth (str): Route to the datafile
        unidad (str, optional): Column to read. Defaults to None.
                                Possibles columns are: AOD_500nm
                                                    AOD_380nm
                                                    PW
                                                    EAE_440_870
                                                    OAM
                                                    Ozone
                                                    NO2

    Returns:
        d: Dataframe of the data
        m: Metadata that is the first 4 rows
    """

    d = pd.read_csv(pth, skiprows=4)

    #getting metadata just in case
    f = open(pth, 'r')
    m = f.readlines()
    m = '  '.join(m[:4])

    #working on reading the data and if necessary filter the data
    d.date_local = pd.to_datetime(d.date_local)
    d.reset_index(inplace=True)
    if not unidad==None:
        #d = d.loc[:, ['time_start', ' time_end', place]]
        d = d.loc[:, ['date_local', unidad]]
    d['numdate'] = mdates.date2num(d.date_local)

    return d, m
'''


if __name__ == '__main__':
    
    #pth = "0_Data\\0_OBS_data\\3_CIMEL\\cimel_La_Paz.csv"
    #d, m = read_cimel(pth, 'Ozone')

    #print(d.head(20))
    #prueba = goes(pth, 'Ancohuma')
    #print(prueba.values)
    #print(prueba.times)
    #print(prueba.df.head())
    tst = read("GOES", "Ancohuma", "Cloud Top Height (ACHA)")
    #tst = read("CIMEL", "La Paz", "AOD_500nm")
    tst.showmetadata()
    