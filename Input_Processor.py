import pandas as pd


class InputProcessor:
    def __init__(self, cur_dict):
        self.final_dict = cur_dict

    def import_files(self, paths: list, names: list) -> dict:
        self.final_dict = {}
        # match data name with dataframe in a dictionary
        for index, name in enumerate(names):
            self.final_dict[name] = pd.read_excel(paths[index])

    def check_files(self):
        # first pass: check if every o+d exists
        odlist = self.final_dict['OD']

