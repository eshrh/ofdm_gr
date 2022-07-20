import pmt
import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='inspect vector',
            in_sig=[(np.complex64, 64)],
            out_sig=[]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

    def work(self, input_items, output_items):
        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        print("START --")
        print(len(input_items[0]), list(map(len, input_items[0])))
        # print("".join(
        #     [f"key: {pmt.to_python(tag.key)}, val: {pmt.to_python(tag.value)}"
        #      for tag in tags]))
        return 0
