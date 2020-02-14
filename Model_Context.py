import Model_State


class Processor:
    def __init__(self):
        # list of inputs
        self.input_list = ['StockInfo', 'TopSH', 'TradableSH', 'ShareChange', 'FutureRep', 'OD', 'SHType']
        # formatted input data
        self.input_data = {}
        # processed data for manual processing use
        self.processed_data = {}
        # processed output data
        self.output_data = {}
        # the main processor
        self.state: Model_State.ModelState = Model_State.ModelState(self)

    def __reset__(self):
