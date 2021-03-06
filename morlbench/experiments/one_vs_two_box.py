#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Nov 19, 2012

@author: Dominik Meyer <meyerd@mytum.de>
"""

import sys
sys.path.append('..')
sys.path.append('.')
import logging as log
import numpy as np

log.basicConfig(level=log.DEBUG)

from plotting_stuff import plot_that_pretty_rldm15

from problems import Newcomb, RandomNewcomb
from agents import OneBoxNewcombAgent, TwoBoxNewcombAgent
from experiment_helpers import interact_multiple


if __name__ == '__main__':
    interactions = 10000

    linspace_from = 0.01
    linspace_to = 0.99
    linspace_steps = 100

    avg_payouts1 = []
    avg_payouts2 = []

    for predictor_accuracy in np.linspace(linspace_from, linspace_to, 
                                          linspace_steps):
        problem1 = RandomNewcomb(predictor_accuracy=predictor_accuracy,
                          payouts=np.array([[1000000, 0], [1001000, 1000]]))
        problem2 = RandomNewcomb(predictor_accuracy=predictor_accuracy,
                          payouts=np.array([[1000000, 0], [1001000, 1000]]))
        agent1 = OneBoxNewcombAgent(problem1)
        agent2 = TwoBoxNewcombAgent(problem2)

        log.info('Playing ...')
        log.info('%s' % (str(agent1)))
        log.info('%s' % (str(problem1)))
        log.info(' VERSUS')
        log.info('%s' % (str(agent2)))
        log.info('%s' % (str(problem2)))

        _, payouts1 = interact_multiple(agent1, problem1, interactions)
        _, payouts2 = interact_multiple(agent2, problem2, interactions)
        avg_payout1 = payouts1.mean(axis=0)
        avg_payout2 = payouts2.mean(axis=0)

        avg_payouts1.append(avg_payout1)
        avg_payouts2.append(avg_payout2)

        log.info('Average Payout: %.3f vs. %.3f' % (avg_payout1, avg_payout2))

    avg_payouts1 = np.array(avg_payouts1)
    avg_payouts2 = np.array(avg_payouts2)

    plot_that_pretty_rldm15([np.linspace(linspace_from, linspace_to,
                                         linspace_steps),
                             np.linspace(linspace_from, linspace_to,
                                         linspace_steps)],
                            [avg_payouts1, avg_payouts2],
                            ["TwoBoxer", "OneBoxer"],
                            "Prediction Accuracy",
                            (0, 1.1, 0.2),
                            "Payout",
                            (0, 1001001, 100000),
                            'one_vs_two_box.pdf')
