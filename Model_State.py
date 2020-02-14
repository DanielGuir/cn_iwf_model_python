import Command
import Model_Context


# classes to track the current state
class ModelState:
    def __init__(self, processor: Model_Context.Processor):
        self.cur_state = 'Undefined'
        self.processor = processor

    def cur_state(self):
        return self.cur_state


# state for uninitialized state (input not verifyed)
class Uninitialized(ModelState):
    def __init__(self, processor: Model_Context.Processor):
        super().__init__(processor)
        self.cur_state = 'Uninitialized'

    def format(self):
        # call format, prompt for input, and reset state if applicable
        return



# input verifyed, ready for process
class Initialized(ModelState):
    def __init__(self, processor: Model_Context.Processor):
        super().__init__(processor)
        self.cur_state = 'Initialized'

    # process the data and generate raw output
    def raw_process(self):
        # process the data and genrate raw output, change state if applicable
        return


class Processed(ModelState):
    def __init__(self, processor: Model_Context.Processor):
        super().__init__(processor)
        self.cur_state = 'Processed'

    # process the data and generate raw output
    def process_individual(self):
        return

    # mark something as completed and sign that one
    def mark_and_sign(self):
        return

    # export to specified location
    def export(self):
        return

    # bring a particular data into user interface
    def (self):

