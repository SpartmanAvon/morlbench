'''
Created on Apr 23, 2015

@author: Dominik Meyer <meyerd@mytum.de>
'''

import numpy as np
import logging as log


def interact_multiple(agent, problem, interactions):
    '''
    Interact multiple times with the problem and then
    return arrays of actions chosen and payouts received
    in each stage.
    '''
    payouts = []
    actions = []
    log.info('Playing %i interactions ... ' % (interactions))
    for t in xrange(interactions):
        action = agent.decide(t)
        payout = problem.play(action)
        agent.learn(t, action, payout)
        log.debug(' step %05i: action: %i, payout: %f' %
                  (t, action, payout))
        payouts.append(payout)
        actions.append(action)
    payouts = np.array(payouts)
    actions = np.array(actions)
    return actions, payouts


def morl_interact_multiple(agent, problem, interactions, trials=100):
    """
    Interact multiple times with the multi objective RL
    problem and then return arrays of actions chosen and
    payouts received in each stage.
    """

    final_rewards = []
    moves = []
    states = []

    for i in xrange(interactions):
        log.info('Playing %i interactions ... ' % i)
        rewards = []
        actions = []
        tmp_states = []
        for t in xrange(trials):
            action = agent.decide(t, problem.state)
            reward = problem.play(action)
            agent.learn(t, action, reward, problem.state)

            log.info('step %04i: state before %i - action %i - payout %s - state %i' %
                      (t, problem.last_state, action, str(reward), problem.state))

            # Preserve reward, action and state
            rewards.append(reward)
            actions.append(action)
            tmp_states.append(problem.last_state)
            # Decide if terminal state
            if problem.terminal_state:
                problem.reset()
                moves.append(actions)
                states.append(tmp_states)
                final_rewards.append(reward)
                break
    return np.array(final_rewards), np.array(moves), np.array(states)



def interact_multiple_twoplayer(agent1, agent2, problem, interactions,
                                use_sum_of_payouts=False):
    '''
    Interact multiple times with the problem and then
    return arrays of actions chosen and payouts received
    in each stage.
    '''
    #TODO: Make this more flexible instead of tedious code duplication.
    payouts1 = []
    actions1 = []
    payouts2 = []
    actions2 = []
    log.info('Playing %i interactions ... ' % (interactions))
    for t in xrange(interactions):
        action1 = agent1.decide(t)
        action2 = agent2.decide(t)
        payout1, payout2 = problem.play(action1, action2)
        if use_sum_of_payouts:
            payoutsum = payout1 + payout2
            agent1.learn(t, action1, payoutsum)
            agent2.learn(t, action2, payoutsum)
        else:
            agent1.learn(t, action1, payout1)
            agent2.learn(t, action2, payout2)
        log.debug(' step %05i: action1: %i, payout1: %i, action2: %i, payout2: \
%i' % (t, action1, payout1, action2, payout2))
        payouts1.append(payout1)
        actions1.append(action1)
        payouts2.append(payout2)
        actions2.append(action2)
    payouts1 = np.array(payouts1)
    actions1 = np.array(actions1)
    payouts2 = np.array(payouts2)
    actions2 = np.array(actions2)
    return (actions1, payouts1), (actions2, payouts2)