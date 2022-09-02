import pandas as pd
import numpy as np

numerical = ['Google PageRank','Trust Metric', 'Citation Flow', 'Spam Score', 'External Backlinks', 'EDU Backlinks',
             'Topic Value', 'Indexed URLs', "has_ip", "url_len", "is_short", "nb_semico", "nb_dslash", "nb_slash",
             "nb_colon", "nb_tilde", "abn_sd", "nb_sd", "nb_dot", "nb_at",
             "nb_and", "nb_equal", "nb_excl", "nb_uscore", "nb_hyphens", "d_ratio", "domain_s", "domain_e",
             "count_https", "nb_hint",]# "nb_brand"]

class DataPrep:

    def cleaning(self, key, column):
        self.df[column] = self.df[column].astype(str)
        new_column = []
        for row in self.df[column]:
            n_row = row.replace(key, "")
            new_column.append(n_row)
        self.df[column] = np.array(new_column, dtype=str)

    def outlier(self, col, df):
        IQR = df[col].quantile(0.75) - df[col].quantile(0.25)
        lower_bound = df[col].quantile(0.25) - (IQR * 1.5)
        upper_bound = df[col].quantile(0.75) + (IQR * 1.5)
        minimum = df[col].min()
        maximum = df[col].max()
        df[col] = np.where(df[col]>upper_bound, upper_bound, df[col])

    def main(self, dataframe):
        self.df = dataframe.copy()
        self.df.drop(self.df[self.df['Trust Metric'] == "Trust Metric:"].index, inplace=True)
        self.cleaning("/10", "Google PageRank")
        self.cleaning(" / 18", "Spam Score")
        self.cleaning(",", "External Backlinks")
        self.cleaning(",", "Indexed URLs")
        self.cleaning(",", "EDU Backlinks")
        
        self.df[numerical] = self.df[numerical].astype(float)
        self.outlier("url_len", self.df)
        
        return self.df


