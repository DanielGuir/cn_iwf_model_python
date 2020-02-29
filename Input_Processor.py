import pandas as pd
import numpy as np


class input_processor:
    # initialize the processor with the data
    def __init__(self, data):
        self.data = data

    # import all files into data
    def import_files(self, path_dict: dict):
        # convert each excel to a dictionary and store in a dataframe
        for key in path_dict:
            # WAND data
            print(key)
            if key in ['AB前十大股东', 'AB股本相关', 'AB十大流通']:
                # read ric as string
                self.data[key] = pd.read_excel(path_dict[key], dtype= {'证券代码': np.dtype(str)})
                cur_df = self.data[key]
                # set index using the number part of ric
                cur_df['index'] = cur_df['证券代码'].map(lambda ric: ric[0:6])
                cur_df.set_index('index', inplace=True)

            # T3 data
            if key in ['CA Share Change CA', 'CN Fame Future Report']:
                # read ric as string
                self.data[key] = pd.read_excel(path_dict[key]) #dtype={'RIC': np.dtype(str)}
                cur_df = self.data[key]
                # set index using the number part of ric
                cur_df['index'] = cur_df['RIC'].map(lambda ric: ric[0:6])
                cur_df.set_index('index', inplace=True)

            # exchange data
            if key in ['CN Ex Shares']:
                # make sure to read ric as string
                self.data[key] = pd.read_excel(path_dict[key], dtype={'证券代码': np.dtype(str)})
                cur_df = self.data[key]
                # set index using the number part of ric
                cur_df['index'] = cur_df['RIC'].map(lambda ric: ric[0:6])
                cur_df.set_index('index', inplace=True)

        # used for method chaining
        return self

    # merge WAND tables, compare with future report and drop unnecessary entries. return number of stocks dropped.
    def merge_tables_and_drop(self):
        df1 = self.data['AB股本相关']
        df2 = self.data['AB前十大股东']
        df3 = self.data['AB十大流通']
        df4 = self.data['CN Fame Future Report']
        # avoid duplicate columns
        cols_to_use_2 = df2.columns.difference(df1.columns)
        cols_to_use_3 = df2.columns.difference(df1.columns)
        # merge 3 WAND tables
        df_merged = df1.merge(df2, left_index=True, right_index=True, on=['证券代码', '证券简称'])\
                       .merge(df3, left_index=True, right_index=True, on=['证券代码', '证券简称'])

        num_before = len(df_merged.index)
        # merge table with future report
        df_dropped = df_merged.merge(df4, left_index=True, right_index=True, how='inner')
        self.data['main_data'] = df_dropped
        return num_before - len(df_dropped.index)





    # verify that data matches
    def verify_match(self):
        return

    def format_data(self):
        return

    # helper function used for debugging
    def debug(self, export_folder):
        return



