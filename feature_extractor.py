import numpy as np
import pandas as pd
import re
import whois
import time
from tqdm.auto import tqdm

import sys
from data_prep import DataPrep 
sys.path.append('./functions')

from feature_functions import FeatureFunctions
from external_functions import ExternalFunctions
from url_parser import UrlParser
from rank import Rank

ranker = Rank()
functions = FeatureFunctions()
ef = ExternalFunctions()
up = UrlParser()

hints = ["porn", "secure", "update", "login", "signin", "bank", "confirm", "verify"]

df_columns = ['has_ip', 'url_len', 'is_short', 'nb_semico', 'nb_dslash', 'nb_slash',
            'nb_colon', 'nb_tilde', 'abn_sd', 'nb_sd', 'nb_dot', 'nb_at', 'nb_and',
            'nb_equal', 'nb_excl', 'nb_uscore', 'nb_hyphens', 'd_ratio', 'domain_s',
            'domain_e', 'count_https', 'nb_hint', 'Google PageRank', 'cPR Score',
            'Domain Authority', 'Page Authority', 'Trust Flow', 'Trust Metric',
            'Citation Flow', 'Domain Validity', 'Global Rank', 'Alexa USA Rank',
            'Alexa Reach Rank', 'Spam Score', 'External Backlinks', 'Referring Domains',
            'EDU Backlinks', 'EDU Domains', 'GOV Backlinks', 'GOV Domains',
            'PR Quality', 'Domain Age', 'HTTP Response Codes:', 'Google Directory listed',
            'DMOZ.org listed', 'Canonical URL',
            'Root IP', 'Title', 'Topic:', 'Topic Value', 'Indexed URLs', 'Crawled Flag']

full_functions = [functions.having_ip_address, functions.url_length, functions.shortening_service,
                functions.count_semicolumn,functions.count_double_slash, functions.count_slash,
                functions.count_colon ,functions.count_tilde,
                functions.abnormal_subdomain, functions.count_subdomain, functions.count_dots,
                functions.count_at,
                functions.count_and, functions.count_equal, functions.count_exclamation,
                functions.count_underscore, functions.count_hyphens,]

base_functions = [functions.ratio_digits, ef.creation_date_len, ef.expiration_date_len,]



class Extraction:

    def url_features(self):
        pbar = tqdm(total=len(self.urls))
        df_list = []
        
        for i in range(len(self.urls)):
            url = self.urls[i]
            p_url = up.return_url_parts(url)
            url_row = []

            ### FUNCTION GROUP ONE FULL URL ###
            for function in full_functions:
                ex_f = lambda arg : function(arg)
                result = ex_f(url)
                url_row.append(result)

            ### FUNCTION GROUP TWO DOMAIN ###
            for function in base_functions:
                ex_f = lambda arg : function(arg)
                try:
                    result = ex_f(p_url["domain"])
                except:
                    result = "unknown"
                url_row.append(result)

            ### OTHER FUNCTIONS ###
            url_row.append(functions.count_http_token(p_url["path"]))
            url_row.append(functions.phish_hints(url, hints))
            #url_row.append(functions.https_token(p_url["protocol"]))

            df_list.append(url_row)
            pbar.update(1)
            
        return df_list

    def rank_features(self):
        input_size = len(self.urls)
        pbar = tqdm(total=input_size)
        df_list = []

        i = 0
        trial = 0
        while i < input_size:
            s_url = self.urls[i]
            domain = ranker.return_url_parts(s_url)["domain"]
            try:
                scraps = ranker.rank_datas(domain, trial)
            except:
                i += 1
                pbar.update(1)
                continue

            if scraps == -1:
                trial = 1
                continue
                
            df_list.append(scraps)
            i += 1
            pbar.update(1)
            trial = 0

        pbar.close()
        return df_list

    def export_dataframe(self, arr1, advanced, arr2=None):
        if advanced:
            df_array = np.concatenate((arr1,arr2),axis=1)
            self.df = pd.DataFrame(df_array, columns=df_columns)
            self.df = self.df.drop(['Topic:', "Title", "Global Rank", "Alexa USA Rank", "Alexa Reach Rank",
                    "Domain Age", "HTTP Response Codes:", "Canonical URL", "Root IP",
                    "Trust Flow", "cPR Score", "Domain Authority", "Page Authority","Referring Domains",
                    'GOV Domains', 'GOV Backlinks', 'EDU Domains'], axis=1)
        else:
            df_array = arr1
            features = ['has_ip','url_len','is_short','nb_semico','nb_dslash','nb_slash','nb_colon',
                        'nb_tilde','abn_sd','nb_sd','nb_dot','nb_at','nb_and','nb_equal','nb_excl',
                        'nb_uscore','nb_hyphens','d_ratio','domain_s','domain_e','count_https','nb_hint']

            self.df = pd.DataFrame(df_array, columns=features)

        return self.df

    def main(self, advanced, file=None, urls=None):
        if file == None:
            self.urls = urls
        elif urls == None:
            self.df = pd.read_csv("data/test.csv")
            self.urls = self.df["url"]
        #

        if advanced == True:
            url_f = self.url_features()
            rank_f = self.rank_features()
            arr1 = np.array(url_f)
            arr2 = np.array(rank_f)
            dataframe = self.export_dataframe(arr1=arr1, arr2=arr2, advanced=advanced)
            return dataframe

        elif advanced == False:
            url_f = self.url_features()
            arr1 = np.array(url_f)
            feature_df = self.export_dataframe(arr1=arr1, advanced=advanced)
            return feature_df

