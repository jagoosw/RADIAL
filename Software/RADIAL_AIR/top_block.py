#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Tue Dec 13 05:36:56 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time

prefix = "/home/pi"

class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(1e9, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.logpwrfft_x_0_1 = logpwrfft.logpwrfft_f(
            sample_rate=samp_rate,
            fft_size=1024,
            ref_scale=2,
            frame_rate=30,
            avg_alpha=1.0,
            average=False,
        )
        self.logpwrfft_x_0_0 = logpwrfft.logpwrfft_f(
            sample_rate=samp_rate,
            fft_size=1024,
            ref_scale=2,
            frame_rate=30,
            avg_alpha=1.0,
            average=False,
        )
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_f(
            sample_rate=samp_rate,
            fft_size=1024,
            ref_scale=2,
            frame_rate=30,
            avg_alpha=1.0,
            average=False,
        )
        self.blocks_float_to_short_0_1 = blocks.float_to_short(1024, 1)
        self.blocks_float_to_short_0_0 = blocks.float_to_short(1024, 1)
        self.blocks_float_to_short_0 = blocks.float_to_short(1024, 1)
        self.blocks_file_sink_1_0 = blocks.file_sink(gr.sizeof_short*1024, prefix+"/Power_detection_bands/cell2.raw", False)
        self.blocks_file_sink_1_0.set_unbuffered(False)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_short*1024, prefix+"/Power_detection_bands/cell1.raw", False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_short*1024, prefix+"/Power_detection_bands/wifi.raw", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.band_pass_filter_2 = filter.fir_filter_fff(1, firdes.band_pass(
            1, 100e6, 20e6, 40e6, 1e6, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_1 = filter.fir_filter_fff(1, firdes.band_pass(
            1, 1800e6, 896e6, 900e6, 1e6, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0 = filter.fir_filter_fff(1, firdes.band_pass(
            1, 4000e6, 1850e6, 1990e6, 1e6, firdes.WIN_HAMMING, 6.76))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.band_pass_filter_0, 0), (self.logpwrfft_x_0_0, 0))    
        self.connect((self.band_pass_filter_1, 0), (self.logpwrfft_x_0_1, 0))    
        self.connect((self.band_pass_filter_2, 0), (self.logpwrfft_x_0, 0))    
        self.connect((self.blocks_complex_to_float_0, 0), (self.band_pass_filter_0, 0))    
        self.connect((self.blocks_complex_to_float_0, 0), (self.band_pass_filter_1, 0))    
        self.connect((self.blocks_complex_to_float_0, 0), (self.band_pass_filter_2, 0))    
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blocks_float_to_short_0_0, 0), (self.blocks_file_sink_1_0, 0))    
        self.connect((self.blocks_float_to_short_0_1, 0), (self.blocks_file_sink_1, 0))    
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_float_to_short_0, 0))    
        self.connect((self.logpwrfft_x_0_0, 0), (self.blocks_float_to_short_0_0, 0))    
        self.connect((self.logpwrfft_x_0_1, 0), (self.blocks_float_to_short_0_1, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.blocks_complex_to_float_0, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.logpwrfft_x_0_0.set_sample_rate(self.samp_rate)
        self.logpwrfft_x_0_1.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()
