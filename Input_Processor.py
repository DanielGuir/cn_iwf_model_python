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
            print(key) # FIXME
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
        # merge table with future report and drop duplicate RIC.
        df_dropped = df_merged.merge(df4, left_index=True, right_index=True, how='inner')
        df_dropped.drop(['证券代码'], inplace=True, axis=1)
        # rename wand datas
        self.rename_and_format(df_dropped)
        self.data['main_data'] = df_dropped
        return num_before - len(df_dropped.index)

    # helper method that formats data in metatable for simplicity.
    # renames column and drops unnecessary column.
    def rename_and_format(self, main_data: pd.DataFrame):
        # rename items from on stockinfo
        main_data.rename(columns={'总股本\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL SHARES',
                                  '流通A股\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL FLOAT A',
                                  '限售A股\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL RESTRICTED A',
                                  'A股合计\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL A',
                                  '流通B股\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL FLOAT B',
                                  '限售B股\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL RESTRICTED B',
                                  'B股合计\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL B',
                                  '香港上市股\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL HK',
                                  '海外上市股\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL OVERSEA',
                                  '流通股合计\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL FLOAT',
                                  '限售股合计\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL RESTRICTED',
                                  '非流通股\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL NONFLOAT',
                                  '自由流通股本\r\n[交易日期] 最新\r\n[单位] 股': 'TOTAL FREE FLOAT',
                                  '定期报告实际披露日期\r\n[报告期] 最新一期(MRQ)': 'MRQ',
                                  '最新报告期\r\n[交易日期] 最新收盘日': 'NEWEST REPORT DAY'},
                         inplace=True)
        # rename spec tab
        for i in range(1, 11):
            main_data.rename(columns={'大股东名称\r\n[日期] 最新\r\n[大股东排名] 第' + str(i) + '名': 'SH1',
                                      '大股东持股数量\r\n[日期] 最新\r\n[大股东排名] 第' + str(i) + '名\r\n[单位] 股': 'SH SHARES1',
                                      '大股东持股比例\r\n[日期] 最新\r\n[大股东排名] 第' + str(i) + '名\r\n[单位] %':  'SH PERCENT1',
                                      '大股东持股股本性质\r\n[日期] 最新\r\n[大股东排名] 第' + str(i) + '名': 'SH SHARE TYPE1',
                                      '大股东持有的限售股份数\r\n[日期] 最新\r\n[大股东排名] 第' + str(i) + '名\r\n[单位] 股': 'SH RESTRICT1',
                                      '流通股东名称\r\n[日期] 最新\r\n[大股东排名] 第' + str(i) + '名': 'FLOATSH1',
                                      '流通股东持股数量\r\n[日期] 最新\r\n[大股东排名] 第' + str(i) + '名\r\n[单位] 股': 'FLOATSH SHARES1',
                                      '流通股东持股比例\r\n[日期] 最新\r\n[大股东排名] 第' + str(i) + '名\r\n[单位] %': 'FLOATSH PERCENT1',
                                      '流通股东持股股本性质\r\n[日期] 最新\r\n[大股东排名] 第' + str(i) + '名': 'FLOATSH SHARETYPE1'},
                             inplace=True)

    # break down shareholder data of each stock into dictionary of dataframes
    # drop corresponding data in metatable after processed
    def generate_subtable(self):
        shareholder_info = {}
        for row in self.data['main_data'].itertuples():
            # initialize data
            sh_name = []
            sh_shares = []
            sh_percent = []
            sh_share_type = []
            sh_restrict = []
            floatsh_name = []
            floatsh_shares = []
            floatsh_percent = []
            floatsh_share_type = []

            for i in range(1, 11):
                sh_empty = False
                float_empty = False
                # load shareholder data
                if not row.loc['SH' + str(i)] == np.nan or row.loc['SH' + str(i)] == "":
                    sh_name.append(row.loc['SH' + str(i)])
                    sh_shares.append(row.loc['SH SHARES' + str(i)])
                    sh_percent.append(row.loc['SH PERCENT' + str(i)])
                    sh_share_type.append(row.loc['SH SHARE TYPE' + str(i)])
                    sh_restrict.append(row.loc['SH RESTRICT' + str(i)])
                else:
                    sh_empty = True

                # load float shareholder data
                if not row.loc['FLOATSH' + str(i)] == np.nan or row.loc['FLOATSH' + str(i)] == "":
                    floatsh_name.append(row.loc['FLOATSH' + str(i)])
                    floatsh_shares.append(row.loc['FLOATSH SHARES' + str(i)])
                    floatsh_percent.append(row.loc['FLOATSH PERCENT' + str(i)])
                    floatsh_share_type.append(row.loc['FLOATSH SHARE TYPE' + str(i)])
                else:
                    float_empty = True

                # if reached the end, stop processing and break out
                if float_empty and sh_empty:
                    break

            result = {}
            result['SHDATA'] = pd.DataFrame({'NAME': sh_name,
                                                       'SHARES': sh_shares,
                                                       'PERCENT': sh_percent,
                                                       'SHARE TYPE': sh_share_type,
                                                       'RESTRICT': sh_restrict})

            result['FLOATSHDATA'] = pd.DataFrame({'NAME': floatsh_name,
                                                       'SHARES': floatsh_shares,
                                                       'PERCENT': floatsh_percent,
                                                       'SHARE TYPE': floatsh_share_type})

            shareholder_info[row.index] = result








    # verify that data matches
    def verify_match(self):
        return

    def format_data(self):
        return

    # helper function used for debugging
    def debug(self, export_folder):
        return



