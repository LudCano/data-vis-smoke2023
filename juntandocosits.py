#MERGING CTH COP
from read_modules import goes
import pandas as pd

anc = goes('Ancohuma')
cth = anc.CTH
cod = anc.COD

cth_d = pd.DataFrame(list(zip(cth.datenum, cth.data)), columns=['datenum','cth'])
cod_d = pd.DataFrame(list(zip(cod.datenum, cod.data)), columns=['datenum','cod'])
cth_d.datenum = cth_d.datenum.astype('float')
cod_d.datenum = cod_d.datenum.astype('float')
#a = cth_d.join(cod_d, on='datenum', how='inner', lsuffix='_left', rsuffix='_right') #ambos 

a = cth_d.merge(cod_d, on='datenum', how='outer') #ambos 