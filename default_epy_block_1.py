import pmt
import numpy as np
from gnuradio import gr


class blk(gr.sync_block):
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1):
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',
            in_sig=[(np.complex64, 64)],
            out_sig=None,
        )
        self.example_param = example_param
        self.message_port_register_out(pmt.intern("messagePort"))

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        pmtmess = pmt.dict_add(pmt.make_dict(),
                               pmt.string_to_symbol("frame_len"),
                               pmt.from_long(int(self.example_param)))
        self.message_port_pub(pmt.intern("messagePort"),
                              pmt.from_long(int(self.example_param)))
        return 0
