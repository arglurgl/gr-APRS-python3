# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: APRS Rx
# Author: Handiko
# Description: www.github.com/handiko/gr-APRS
# GNU Radio version: 3.10.1.1

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from AFSK_Demod import AFSK_Demod  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal







class APRS_Rx(gr.hier_block2):
    def __init__(self, baud=1200, gmu=0.175, mark=1200, mu=0.5, samp_rate=24e3, space=2400):
        gr.hier_block2.__init__(
            self, "APRS Rx",
                gr.io_signature(1, 1, gr.sizeof_float*1),
                gr.io_signature.makev(2, 2, [gr.sizeof_float*1, gr.sizeof_float*1]),
        )
        self.message_port_register_hier_out("HDLC")

        ##################################################
        # Parameters
        ##################################################
        self.baud = baud
        self.gmu = gmu
        self.mark = mark
        self.mu = mu
        self.samp_rate = samp_rate
        self.space = space

        ##################################################
        # Blocks
        ##################################################
        self.digital_hdlc_deframer_bp_0 = digital.hdlc_deframer_bp(32, 500)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2, digital.DIFF_DIFFERENTIAL)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(2*(1+0.0), 0.25*gmu*gmu, mu, gmu, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_not_xx_0 = blocks.not_bb()
        self.blocks_and_const_xx_0 = blocks.and_const_bb(1)
        self.AFSK_Demod_0 = AFSK_Demod(
            baud=baud,
            fsk_hi_tone=space,
            fsk_lo_tone=mark,
            in_sps=int(samp_rate/baud),
            out_sps=2,
        )


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self, 'HDLC'))
        self.connect((self.AFSK_Demod_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.AFSK_Demod_0, 0), (self, 1))
        self.connect((self.blocks_and_const_xx_0, 0), (self.digital_hdlc_deframer_bp_0, 0))
        self.connect((self.blocks_not_xx_0, 0), (self.blocks_and_const_xx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_not_xx_0, 0))
        self.connect((self, 0), (self.AFSK_Demod_0, 0))


    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.AFSK_Demod_0.set_baud(self.baud)
        self.AFSK_Demod_0.set_in_sps(int(self.samp_rate/self.baud))

    def get_gmu(self):
        return self.gmu

    def set_gmu(self, gmu):
        self.gmu = gmu
        self.digital_clock_recovery_mm_xx_0.set_gain_omega(0.25*self.gmu*self.gmu)
        self.digital_clock_recovery_mm_xx_0.set_gain_mu(self.gmu)

    def get_mark(self):
        return self.mark

    def set_mark(self, mark):
        self.mark = mark
        self.AFSK_Demod_0.set_fsk_lo_tone(self.mark)

    def get_mu(self):
        return self.mu

    def set_mu(self, mu):
        self.mu = mu
        self.digital_clock_recovery_mm_xx_0.set_mu(self.mu)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.AFSK_Demod_0.set_in_sps(int(self.samp_rate/self.baud))

    def get_space(self):
        return self.space

    def set_space(self, space):
        self.space = space
        self.AFSK_Demod_0.set_fsk_hi_tone(self.space)

