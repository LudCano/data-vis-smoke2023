

import pandas as pd
import matplotlib.dates as mdates


tab = pd.read_csv('data.csv')
varss = tab.variable.unique()
places = tab.place.unique()
origin = tab.origin.unique()


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



if __name__ == '__main__':
    #pth = '0_Data\\3_SATELLITE_data\\1_GOES\\COD_stations.csv'
    #d, m = read_goes(pth, 'Ancohuma')

    pth = "0_Data\\0_OBS_data\\3_CIMEL\\cimel_La_Paz.csv"
    d, m = read_cimel(pth, 'Ozone')

    #print(d.head(20))