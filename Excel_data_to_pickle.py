import pandas as pd
import pickle

file_name = 'RS and FS neuron trace for modeling.xlsx'
acc_fs = pd.read_excel(file_name, sheet_name='ACC FS neuron')
ppc_fs = pd.read_excel(file_name, sheet_name='PPC FS neuron')
acc_rs = pd.read_excel(file_name, sheet_name='ACC RS neuron')
ppc_rs = pd.read_excel(file_name, sheet_name='PPC RS neuron')

slice_data = {}  # make a dictionary 

slice_data['PPC_FS'] = ppc_fs
slice_data['ACC_RS'] = acc_rs
slice_data['PPC_RS'] = ppc_rs
slice_data['ACC_FS'] = acc_fs

with open('slice_data.pickle', 'wb') as handle:
    pickle.dump(slice_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

