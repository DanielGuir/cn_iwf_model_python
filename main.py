import threading
import Input_Processor as ip
import pandas as pd
if __name__ == "__main__":

    data = {}
    path = {'AB前十大股东': 'Raw_Data_Examples\AB前十大股东_20190719.xlsx',
            'AB股本相关': 'Raw_Data_Examples\AB股本相关_20190719.xlsx',
            'AB十大流通': 'Raw_Data_Examples\AB十大流通_20190719.xlsx',
            #'CA Share Change CA': 'Raw_Data_Examples\CA Share Change CA_20190719.xls',
            'CN Fame Future Report': 'Raw_Data_Examples\CN FAME Future Report_20190719.xls'}
            #'CN Ex Shares': 'Raw_Data_Examples\CN EX Shares_20190719.xls'}
    input_processor = ip.input_processor(data)

    print('Num deleted' + str(input_processor.import_files(path).merge_tables_and_drop()))
    #print(data['main_data'])
    data['main_data'].to_excel('Test.xlsx')

