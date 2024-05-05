import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import datetime as dt
import pytz
def get_times(pth):
    d = pd.read_csv(pth, skiprows=6)

    #working on reading the data and if necessary filter the data
    d.time_start = pd.to_datetime(d.time_start)
    d = d.sort_values('time_start')
    d.reset_index(inplace=True)
    datenum = mdates.date2num(d.time_start)
    return datenum, d.time_start

class measurement:
    def __init__(self, place, fullname, units, pth):
        self.full_name = fullname
        self.units = units
        d = pd.read_csv(pth, skiprows=6)

        #getting metadata just in case
        f = open(pth, 'r')
        m = f.readlines()
        self._metadata = m[:6]

        #working on reading the data and if necessary filter the data
        d.time_start = pd.to_datetime(d.time_start)
        d = d.sort_values('time_start')
        d.reset_index(inplace=True)
        self.times = d.time_start.to_list()
        place = " " + place
        self.data = np.array(d[place])
        self.datenum = mdates.date2num(d.time_start)
        d = d.loc[:, ['time_start', place]]
        d['datenum'] = mdates.date2num(d.time_start)
        self.df = d
        self.path = pth
        self.units = units

    def trim(self, idx0, idxf):
        self.data = self.data[idx0:idxf]

    def metadata(self):
        for i in self._metadata:
            print(i)

class goes:
    def __init__(self, place):
        table = pd.read_csv('data.csv')
        go = table[table.origin == 'GOES']
        go = go[go.place == place]
        var_names = go.variable
        units = go.units
        pths = go.path
        codes = [i.split('/')[-1].split('_')[0] for i in pths]
        
        for i, u, v, pt in zip(codes, units, var_names, pths):
            setattr(self, i, measurement(place, v, u, pt))

        datenum, times = get_times(pt)
        self.codes = codes
        self.datenum = datenum
        self.times_utc = times
        self.times_local = pd.Series([i + dt.timedelta(hours = -4) for i in times])
        self.variables = var_names.to_list()
        self.vars_codes = "\n".join([j + "-->" + i for i,j in zip(var_names, codes)])

    def show_vars(self):
        for i,j in zip(self.variables, self.codes):
            print(i, " --> ", j)

    def trim_times(self, dstart, dfinal):
        def inner_trim(self, d0, df):
            #l = self.times_local[self.times_local > d0]
            msk = self.times_local[(self.times_local > d0) & (self.times_local < df)]
            self.times_local = msk
            idx0 = msk.index[0]
            idxf = msk.index[-1]
            self.times_utc = self.times_utc[idx0:idxf]
            for i in self.codes:
                self.__dict__[i].data = self.__dict__[i].data[idx0:idxf+1]
                
        d0 = pd.Timestamp(dstart, tz = -4)
        df = pd.Timestamp(dfinal, tz = -4)
        inner_trim(self,d0, df)


