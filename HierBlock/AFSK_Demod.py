# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Filterbank AFSK Demodulator
# Author: Handiko
# GNU Radio version: 3.10.1.1

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
import math







class AFSK_Demod(gr.hier_block2):
    def __init__(self, baud=1200, fsk_hi_tone=2200, fsk_lo_tone=1200, in_sps=40, out_sps=2):
        gr.hier_block2.__init__(
            self, "Filterbank AFSK Demodulator",
                gr.io_signature(1, 1, gr.sizeof_float*1),
                gr.io_signature(1, 1, gr.sizeof_float*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.baud = baud
        self.fsk_hi_tone = fsk_hi_tone
        self.fsk_lo_tone = fsk_lo_tone
        self.in_sps = in_sps
        self.out_sps = out_sps

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = baud*in_sps
        self.decay = decay = 10e-6 + 0*2e-2
        self.attack = attack = 0.5 + 0*1e-4

        ##################################################
        # Blocks
        ##################################################
        self.root_raised_cosine_filter_1 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                in_sps*1.0,
                1.0,
                0.7,
                4*in_sps))
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                in_sps*1.0,
                1.0,
                0.7,
                4*in_sps))
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=out_sps,
                decimation=in_sps,
                taps=[],
                fractional_bw=0)
        self.blocks_sub_xx_2 = blocks.sub_ff(1)
        self.blocks_rotator_cc_1 = blocks.rotator_cc((-1.0*fsk_hi_tone/samp_rate)*2*math.pi, False)
        self.blocks_rotator_cc_0 = blocks.rotator_cc((-1.0*fsk_lo_tone/samp_rate)*2*math.pi, False)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_mag_1 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.analog_agc2_xx_1 = analog.agc2_ff(attack, decay, 0.5, 1.0)
        self.analog_agc2_xx_1.set_max_gain(65536)
        self.analog_agc2_xx_0 = analog.agc2_ff(attack, decay, 0.5, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.blocks_sub_xx_2, 0))
        self.connect((self.analog_agc2_xx_1, 0), (self.blocks_sub_xx_2, 1))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_1, 0), (self.analog_agc2_xx_1, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_rotator_cc_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_rotator_cc_1, 0))
        self.connect((self.blocks_rotator_cc_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.blocks_rotator_cc_1, 0), (self.root_raised_cosine_filter_1, 0))
        self.connect((self.blocks_sub_xx_2, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.root_raised_cosine_filter_1, 0), (self.blocks_complex_to_mag_1, 0))


    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.set_samp_rate(self.baud*self.in_sps)

    def get_fsk_hi_tone(self):
        return self.fsk_hi_tone

    def set_fsk_hi_tone(self, fsk_hi_tone):
        self.fsk_hi_tone = fsk_hi_tone
        self.blocks_rotator_cc_1.set_phase_inc((-1.0*self.fsk_hi_tone/self.samp_rate)*2*math.pi)

    def get_fsk_lo_tone(self):
        return self.fsk_lo_tone

    def set_fsk_lo_tone(self, fsk_lo_tone):
        self.fsk_lo_tone = fsk_lo_tone
        self.blocks_rotator_cc_0.set_phase_inc((-1.0*self.fsk_lo_tone/self.samp_rate)*2*math.pi)

    def get_in_sps(self):
        return self.in_sps

    def set_in_sps(self, in_sps):
        self.in_sps = in_sps
        self.set_samp_rate(self.baud*self.in_sps)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.in_sps*1.0, 1.0, 0.7, 4*self.in_sps))
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.in_sps*1.0, 1.0, 0.7, 4*self.in_sps))

    def get_out_sps(self):
        return self.out_sps

    def set_out_sps(self, out_sps):
        self.out_sps = out_sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_rotator_cc_0.set_phase_inc((-1.0*self.fsk_lo_tone/self.samp_rate)*2*math.pi)
        self.blocks_rotator_cc_1.set_phase_inc((-1.0*self.fsk_hi_tone/self.samp_rate)*2*math.pi)

    def get_decay(self):
        return self.decay

    def set_decay(self, decay):
        self.decay = decay
        self.analog_agc2_xx_0.set_decay_rate(self.decay)
        self.analog_agc2_xx_1.set_decay_rate(self.decay)

    def get_attack(self):
        return self.attack

    def set_attack(self, attack):
        self.attack = attack
        self.analog_agc2_xx_0.set_attack_rate(self.attack)
        self.analog_agc2_xx_1.set_attack_rate(self.attack)

