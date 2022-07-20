#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: ofdm
# Author: Eshan Ramesh
# GNU Radio version: v3.11.0.0git-186-g4f125b36

from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import default_epy_block_0_0 as epy_block_0_0  # embedded python block
import default_epy_block_1 as epy_block_1  # embedded python block
import numpy as np




class default(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "ofdm", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.payload_mod = payload_mod = digital.constellation_bpsk()
        self.occupied_carriers = occupied_carriers = (list(range(-26, -21)) + list(range(-20, -7)) + list(range(-6, 0)) + list(range(1, 7)) + list(range(8, 21)) + list(range(22, 27)),)
        self.header_mod = header_mod = digital.constellation_bpsk()
        self.sync_word2 = sync_word2 = [np.random.choice([-1, 1]) if (x in occupied_carriers[0]+[-21, -7, 7, 21]) else 0 for x in range(-32, 32)]
        self.sync_word1 = sync_word1 = [np.sqrt(2) * np.random.choice([-1, 1]) if (x in occupied_carriers[0]+[-21, -7, 7, 21] and x % 2 == 0) else 0 for x in range(-32, 32)]
        self.samp_rate = samp_rate = 32000
        self.pilot_symbols = pilot_symbols = ((1, 1, 1, -1,),)
        self.pilot_carriers = pilot_carriers = ((-21, -7, 7, 21,),)
        self.header_formatter = header_formatter = digital.packet_header_ofdm(occupied_carriers, n_syms=1, len_tag_key="packet_len", frame_len_tag_key="frame_len", bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol())
        self.fft_len = fft_len = 64

        ##################################################
        # Blocks
        ##################################################
        self.fft_vxx_0 = fft.fft_vcc(fft_len, False, (), True, 1)
        self.epy_block_1 = epy_block_1.blk(example_param=1.0)
        self.epy_block_0_0 = epy_block_0_0.blk()
        self.digital_packet_headergenerator_bb_0_0 = digital.packet_headergenerator_bb(header_formatter.base(), "packet_len")
        self.digital_ofdm_sync_sc_cfb_0 = digital.ofdm_sync_sc_cfb(64, 16, True, 0.9)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(
            fft_len,
            ((fft_len//4),),
            0,
            '')
        self.digital_ofdm_carrier_allocator_cvc_0_0 = digital.ofdm_carrier_allocator_cvc( fft_len, occupied_carriers, pilot_carriers, pilot_symbols, (sync_word1, sync_word2), 'packet_len', True)
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
            3,
            64,
            16,
            "",
            "",
            True,
            gr.sizeof_gr_complex,
            "rx_time",
            samp_rate,
            [],
            0)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(payload_mod.points(), 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(header_mod.points(), 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, "packet_len", 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 2, "packet_len")
        self.blocks_null_sink_2 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_gr_complex*64)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*64)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/esrh/arcom/ofdm_rewrite/int_ones.bin', False, 0, 2)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 80)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc((-2/fft_len))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_1, 'messagePort'), (self.digital_header_payload_demux_0, 'header_data'))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.digital_ofdm_sync_sc_cfb_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_packet_headergenerator_bb_0_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.blocks_null_sink_1, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.epy_block_0_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.epy_block_1, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0, 2), (self.blocks_null_sink_2, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0, 1), (self.digital_header_payload_demux_0, 1))
        self.connect((self.digital_packet_headergenerator_bb_0_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))


    def get_payload_mod(self):
        return self.payload_mod

    def set_payload_mod(self, payload_mod):
        self.payload_mod = payload_mod

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, n_syms=1, len_tag_key="packet_len", frame_len_tag_key="frame_len", bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol()))
        self.set_sync_word1([np.sqrt(2) * np.random.choice([-1, 1]) if (x in self.occupied_carriers[0]+[-21, -7, 7, 21] and x % 2 == 0) else 0 for x in range(-32, 32)])
        self.set_sync_word2([np.random.choice([-1, 1]) if (x in self.occupied_carriers[0]+[-21, -7, 7, 21]) else 0 for x in range(-32, 32)])

    def get_header_mod(self):
        return self.header_mod

    def set_header_mod(self, header_mod):
        self.header_mod = header_mod

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers

    def get_header_formatter(self):
        return self.header_formatter

    def set_header_formatter(self, header_formatter):
        self.header_formatter = header_formatter

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.analog_frequency_modulator_fc_0.set_sensitivity((-2/self.fft_len))




def main(top_block_cls=default, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
