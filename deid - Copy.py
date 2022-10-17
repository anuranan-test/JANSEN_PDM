import os
import sys
import config
import pandas as pd
import numpy as np

sys.path.insert(0, os.getcwd())


class deid:

    def __init__(self):
        self.mask_list = config.mask


    def mask(self, df):
        for masking in self.mask_list:
            df[masking] = np.nan
            # print(df)

    def load_data(self):
        global df
        global sht_nm
        global file_nm
        file_nm = input('Please Enter File Name:\n')
        sht_nm = input('Please Enter Excel Sheet Name:\n')
        df = pd.DataFrame()
        df = pd.read_excel(str(os.getcwd()+'\\Input\\'+ file_nm +config.extension), sheet_name=sht_nm)
        # print(df)

    def rollup(self, df):
        for year in config.roll_up:
            df[year] = df[year].astype('str')
            df[year] = df[year].str[:4]+'0101'
            # print(df[year])
        for zips in config.pat_zip:
            df[zips] = df[zips].astype('str')
            df[zips] = df[zips].str[1:]
            df[zips] = df[zips].str[:3]
            # print(df[zips])

    def write(self, df):
        df.to_excel(sht_nm+'_deid'+config.extension, index=False)

    def execute(self):
        self.load_data()
        self.mask(df)
        self.rollup(df)
        self.write(df)


