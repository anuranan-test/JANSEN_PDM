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
        # df = pd.read_excel(str(os.getcwd() + '\\Input\\' + 'Sample Data_JP' + config.extension), sheet_name='Patient Demogrpahics_Hiragana')
        # print(df)

    def rollup(self, df):
        for year in config.roll_up:
            df[year] = df[year].astype('str')
            # for dates in df[year]:
            #     dates = datetime.strptime(dates, '%d/%m/%y')
            #     dates = datetime.datetime.strptime(df[year], "%m/%d/%y").date()
            df[year] = df[year].str[-4:]+'0101'
            print('YEARS ====')
            print(df[year])
            # datetime.datetime.strptime(year[], '%y').strftime('%Y-%m-%d')
            # print(df[year])
        print(config.restricted_zips.keys())
        for zips in config.pat_zip:
            df[zips] = df[zips].astype('str')
            df[zips] = df[zips].str[1:]
            df[zips] = df[zips].str[:2]
            df.replace({zips: config.restricted_zips})
            for zip_code in df[zips]:
                if str(zip_code) in config.restricted_zips.keys():
                    # print(str(zip_code) + '= current zip to be changed')
                    df.loc[df[zips] == str(zip_code), zips] = str(config.restricted_zips[zip_code])
                    # print(df.at[zip_code, zips] + '=')
                    # df[zips] = df[zips].apply(lambda x: config.restricted_zips.get(x))
            #     if df.loc(zip_code, zips) in config.restricted_zips:
            #         df[zip_code][zips] = df[zip_code][zips].map(config.restricted_zips)
        # df.applymap(lambda x: config.restricted_zips.get(x))
            # print(df[zips])

    def write(self, df):
        df.to_excel(sht_nm+'_deid'+config.extension, index=False)
        # df.to_excel('Patient Demogrpahicchs_Hiragana' + '_deid' + config.extension, index=False)

    def translate(self, df):
        translator = Translator()
        translations = {}
        for column in df.columns:
            if column not in config.translate_cols:
                continue
            unique_elements = df[column].unique()
            for element in unique_elements:
                timeout = httpx.Timeout(5)
                # element = element.replace('令和', '').replace('昭和', '').replace('平成', '')
                element = element.replace('邮编', '')
                print('Translating  : ', element, '\n')
                translations[element] = translator.translate(element, target='en').text
                print('translated element : ', translations[element], '\n')
        df.replace(translations, inplace=True)
        print('Translation Completed')

    def hash(self, df):
        for col in config.hashed_cols:
            df[col.strip()] = df[col.strip()].apply(
                # lambda x: '0x' + hashlib.md5((str(x) + str(config.salt)).encode()).hexdigest().upper())
                lambda x: '0x' + hashlib.sha256((str(x) + str(config.salt)).encode()).hexdigest().upper())

    def execute(self):
        self.load_data()
        self.translate(df)
        self.mask(df)
        self.rollup(df)
        self.hash(df)
        self.write(df)



