import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import datetime as dt

def get_times(pth):
    d = pd.read_csv(pth, skiprows=6)

    #working on reading the data and if necessary filter the data
    d.time_start = pd.to_datetime(d.time_start)
    d = d.sort_values('time_start')
    d.reset_index(inplace=True)
    datenum = mdates.date2num(d.time_start)
    return datenum, d.time_start

class measurement_goes:
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
        d.time_start = d.time_start + dt.timedelta(hours = -4)
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
            setattr(self, i, measurement_goes(place, v, u, pt))

        datenum, times = get_times(pt)
        self.codes = codes
        self.datenum = datenum
        self.times_utc = times
        self.times_local = pd.Series([i + dt.timedelta(hours = -4) for i in times])
        self.variables = var_names.to_list()
        #self.vars_codes = "\n".join([j + "-->" + i for i,j in zip(var_names, codes)])

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



class measurement_cimel:
    def __init__(self, df, cod, va, un, codes_lst,m):
        self.units = un
        self.full_name = va
        cols = ["AOD_500nm","AOD_380nm","PW","EAE_440_870","OAM","Ozone","NO2"]
        dc = {i:j for i,j in zip(codes_lst, cols)} #creando un diccionario para relacionarlos
        col = dc[cod]
        self.data = np.array(df[col])
        self.df = df.loc[:, ['date_local', col]]
        self.times = pd.to_datetime(df.date_local)
        self.datenum = mdates.date2num(self.times)
        self._metadata = m

    def trim(self, idx0, idxf):
        self.data = self.data[idx0:idxf]

    def metadata(self):
        for i in self._metadata:
            print(i)
       

class cimel:
    def __init__(self,place):
        table = pd.read_csv('data.csv')
        go = table[table.origin == 'CIMEL']
        go = go[go.place == place]
        var_names = go.variable
        units = go.units
        df_all = pd.read_csv(go.path.to_list()[0], skiprows=4)
        codes = go.code.to_list()
        f = open(go.path.to_list()[0], 'r')
        m = f.readlines()[:4]
        
        for i, u, v, pt in zip(codes, units, var_names, df_all):
            setattr(self, i, measurement_cimel(df_all, i, v, u, codes,m))

        self.times_local = pd.to_datetime(df_all.date_local)
        self.times_utc = [i + dt.timedelta(hours=+4) for i in self.times_local]
        self.datenum = mdates.date2num(self.times_local)
        self.variables = var_names.to_list()
        self.codes = codes
        
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
                
        d0 = pd.Timestamp(dstart)
        df = pd.Timestamp(dfinal)
        inner_trim(self,d0, df)

