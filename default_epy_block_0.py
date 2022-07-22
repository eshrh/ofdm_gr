import pmt
import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='inspect vector',
            in_sig=[(np.complex64, 64)],
            out_sig=None)

    def work(self, input_items, output_items):
        print("START--")
        print(len(input_items[0]), list(map(len, input_items[0])))
        print(input_items[0][0])
        return 0
