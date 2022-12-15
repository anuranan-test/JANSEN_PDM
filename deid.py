import os
import sys
import config
import pandas as pd
import numpy as np
import httpx
import hashlib
# import datetime
from googletrans import Translator
# import translators
# import re
from simple_salesforce import Salesforce

sys.path.insert(0, os.getcwd())




class deid:

    def __init__(self):
        self.mask_list = config.mask


    def mask(self, df):
        for masking in self.mask_list:
            df[masking] = np.nan

    def salesforce_filecreat(self):

        SALESFORCE_EMAIL = input('Enter SALESFORCE_EMAIL: \t')
        SALESFORCE_TOKEN = input('Enter SALESFORCE_TOKEN: \t')
        SALESFORCE_PASSWORD = input('Enter SALESFORCE_PASSWORD: \t')

        sf = Salesforce(username=SALESFORCE_EMAIL, password=SALESFORCE_PASSWORD, security_token=SALESFORCE_TOKEN)

        get_query = '''SELECT FirstName,LastName,PersonMobilePhone,Phone,PersonEmail,PersonBirthdate,Postal_Code__c,
        PxP_Postal_Code_other__c ,PxP_City__c ,PxP_Country_other__c from Account
        '''
        query_result = sf.query(get_query)
        sf_df = pd.DataFrame(query_result)
        sf_df.to_excel('salesforce.xlsx', index=False)

    def load_data(self):
        global df
        global sht_nm
        global file_nm
        print('Path = '+str(os.getcwd()))
        # file_nm = input('Please Enter File Name:\n')
        # sht_nm = input('Please Enter Excel Sheet Name:\n')
        df = pd.DataFrame()
        # df = pd.read_excel(str(os.getcwd()+'\\Input\\'+ file_nm +config.extension), sheet_name=sht_nm)
        df = pd.read_excel(str(os.getcwd()+ '\\salesforce.xlsx'), sheet_name='Sheet1')
        # df = pd.read_excel(str(os.getcwd() + '\\Input\\' + 'Sample Data_JP' + config.extension), sheet_name='Patient Demogrpahics_Hiragana')

    def rollup(self, df):
        for year in config.roll_up:
            df[year] = df[year].astype('str')
            df[year] = df[year].str[-4:]+'0101'
            print('YEARS ====')
            print(df[year])
        print(config.restricted_zips.keys())
        for zips in config.pat_zip:
            print(str(df[zips]))
            df[zips] = df[zips].apply(lambda x: str(x).replace("邮编", "")).apply(lambda x: str(x).replace("令和", ""))\
                .apply(lambda x: str(x).replace("昭和", "")).apply(lambda x: str(x).replace("平成", ""))\
                .apply(lambda x: str(x).strip())
            print(str(df[zips]))
            df[zips] = df[zips].astype('str')
            df[zips] = df[zips].str[:3]
            print(str(df[zips]))
            df.replace({zips: config.restricted_zips})
            for zip_code in df[zips]:
                if str(zip_code) in config.restricted_zips.keys():
                    df.loc[df[zips] == str(zip_code), zips] = str(config.restricted_zips[zip_code])

    def write(self, df):
        df.to_excel(sht_nm+'_deid'+config.extension, index=False)
        # df.to_excel('Patient Demogrpahicchs_Hiragana' + '_deid' + config.extension, index=False)

    def translate(self, df):
        if "chinese" not in file_nm:
            translator = Translator()
            translations = {}
            for column in df.columns:
                if column not in config.translate_cols:
                    continue
                unique_elements = df[column].unique()
                for element in unique_elements:
                    timeout = httpx.Timeout(5)
                    print('Translating  : ', element, '\n')
                    translations[element] = translator.translate(element, target='en').text
                    print('translated element : ', translations[element], '\n')
            df.replace(translations, inplace=True)
            print('Translation Completed')
        elif "chinese" in file_nm:
            print('Using Argotranslate:')
            translations = {}
            for column in df.columns:
                if column not in config.translate_cols:
                    continue
                unique_elements = df[column].unique()
                for element in unique_elements:
                    timeout = httpx.Timeout(5)
                    print('ChinaTranslating  : ', element, '\n')
                    translations[element] = translators.youdao(str(element), dest = 'en')
                    print('Chinatranslated element : ', translations[element], '\n')
                df.replace(translations, inplace=True)
            print('ChinaTranslation Completed')

    def hash(self, df):
        for col in config.hashed_cols:
            df[col.strip()] = df[col.strip()].apply(
                lambda x: '0x' + hashlib.sha256((str(x) + str(config.salt)).encode()).hexdigest().upper())

    def execute(self):
        self.salesforce_filecreat()
        self.load_data()
        # self.translate(df)
        self.mask(df)
        self.rollup(df)
        self.hash(df)
        self.write(df)
