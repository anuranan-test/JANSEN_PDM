import os
import sys
import config
import pandas as pd
import numpy as np
import httpx
import hashlib
import datetime
from googletrans import Translator

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
            df[year] = df[year].str[-4:]+'0101'
            # datetime.datetime.strptime(year[], '%y').strftime('%Y-%m-%d')
            # print(df[year])
        for zips in config.pat_zip:
            df[zips] = df[zips].astype('str')
            df[zips] = df[zips].str[1:]
            df[zips] = df[zips].str[:2]
            # print(df[zips])

    def write(self, df):
        df.to_excel(sht_nm+'_deid'+config.extension, index=False)

    def translate(self, df):
        translator = Translator()
        translations = {}
        for column in df.columns:
            if column not in config.translate_cols:
                continue
            unique_elements = df[column].unique()
            for element in unique_elements:
                timeout = httpx.Timeout(5)
                print('Translating  : ', element, '\n')
                translations[element] = translator.translate(element, source='ja', target='en').text
                print('translated element : ', translations[element], '\n')
        df.replace(translations, inplace=True)
        print('Translation Completed')

    def hash(self, df):
        for col in config.hashed_cols:
            df[col.strip()] = df[col.strip()].apply(
                lambda x: '0x' + hashlib.md5((str(x) + str(config.salt)).encode()).hexdigest().upper())

    def execute(self):
        self.load_data()
        self.translate(df)
        self.mask(df)
        self.rollup(df)
        self.hash(df)
        self.write(df)



