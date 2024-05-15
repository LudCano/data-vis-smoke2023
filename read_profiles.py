import pandas as pd
import matplotlib.dates as mdates
import numpy as np
import datetime as dt


def pressure_to_altitude(pressure):
    h = (1-((pressure/1013.25)**0.190284))*145366.45*0.3048
    return h

def alt_to_press(altitude):
    p = (((1- altitude/(145366.45*0.3048)))**(1/0.190284))*1013.25
    return p
            

class vert_profs:

    def __init__(self, place):
        pth = f'0_Data/3_SATELLITE_data/1_GOES/Humedad_perfil_vertical/{place}_stations.csv'

        d = pd.read_csv(pth, skiprows=7)
        d.time_start = pd.to_datetime(d.time_start)
        times = d.time_start
        d = d.sort_values('time_start')
        times = d.time_start.to_list()
        d = d.iloc[:,2:]
        d.dropna(axis = 1, inplace=True)
        pressures = np.array([float(i) for i in d.columns])
        a = d.to_numpy(dtype=float)
        altitudes = pressure_to_altitude(pressures)
        t_nums = mdates.date2num(times)
        t0 = dt.datetime.combine(times[0], dt.time(0))
        tf = dt.datetime.combine(times[-1], dt.time(times[-1].hour))
        ti = t0
        hourly_times = []
        mean_mtx = []
        while ti<tf:
            hourly_times.append(ti)
            
            tx = ti + dt.timedelta(hours=1)
            lim0 = mdates.date2num(ti)
            limf = mdates.date2num(tx)
            aaa = np.where((lim0 <= t_nums) & (t_nums <= limf))[0]
            ti = tx
            
            mean_prof = np.nanmean(a[aaa[0]:aaa[-1]+1,:],axis=0)
            mean_mtx.append(mean_prof)
        #hourly_times.append(tf)
        mean_mtx = np.array(mean_mtx)
        self.times = hourly_times
        self.data = mean_mtx
        self.altitudes = altitudes
        self.all_data = a
        self.all_times = times
        self.pressures = pressures



    


if __name__ == "__main__":
    a = vert_profs('Ancohuma')
    print(a.pressures.shape)
