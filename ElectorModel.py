'''
Affinity conclave voting model:
===============================

The model is composed of a set of electors E and options O for them to vote 
on. Each elector e_i has a set of opinions o_ji which represents its preference
for option j. 

Initially, each elector chooses an option at random, with probabilities
proportional to its preferences. In each subsequent round, agents vote for the
option that maximizes v_j * o_ji where v_j is the votes that option j received 
last round.
'''

from __future__ import division
import random

class Elector(object):
    '''
    Elector agent.
    '''

    def _weighted_random(self, weight_dict):
        '''
        Chooses a possibility based on their associated weights.

        Args:
            weight_dict: A dictionary of the form
                    {Outcome1: weight1, Outcome2: weight2}
                Note that weights must not sum to 1; this method
                scales them automatically.
        Returns:
            One of the outcomes specified in weight_dict
        '''
        total = sum(weight_dict.values())
        choice = random.random() * total
        counter = 0
        for outcome, weight in weight_dict.items():
            if choice < counter + weight:
                return outcome
            else:
                counter += weight

    def __init__(self, opinions=None):
        '''
        Initialize an Elector agent.

        Args:
            opinions: A dictionary of the form
                {option1: preference, option2: prefernce}
        '''

        self.opinions = opinions

    def first_pick(self):
        '''
        Choose an initial vote.
        Return:
            An option chosen randomly in proportion to the opinion.
        '''
        return self._weighted_random(self.opinions)

    def next_vote(self, previous_votes):
        '''
        Decide the next vote given the outcome of the previous vote.
        Args:
            previous_votes: A dictionary associating outcomes with votes:
                {option1: votes for option1, option2: votes for option 2...}

        Returns:
            The option that maximizes votes * preference
        '''
        max_weight = 0
        max_outcome = None

        for option, pref in self.opinions.items():
            wgt = pref * previous_votes[option]
            if wgt > max_weight:
                max_outcome = option
                max_weight = wgt

        return max_outcome


class Election(object):
    '''
    Supervisor class for elections.
    '''

    def __init__(self, options, fraction_required=0.5, max_rounds=None):
        '''
        Initiate a new election model.
        Args:
            options: List of possible outcomes to be voted on
            fraction_required: Percent of votes needed to win
            max_rounds: Maximum number of rounds of voting.
        '''

        self.options = options
        self.electors = {}
        self.rounds = 0
        self.elector_count = 0
        self.fraction_required = fraction_required
        self.max_rounds = max_rounds
        self.vote_rounds = []

    def add_elector(self, preference_set, name=None):
        '''
        Add a new elector with the given prefernce set.
        Args:
            preference_set: A preference set dictionary
            name: Name for the agent, if not just a number.
        '''
        if name is None:
            name = self.elector_count

        new_elector = Elector(preference_set)
        self.electors[name] = new_elector
        self.elector_count += 1

    def vote(self):
        '''
        A single round of voting.
        '''
        votes = {}
        for option in self.options:
            votes[option] = 0

        for elector in self.electors.values():
            if self.rounds == 0:
                vote = elector.first_pick()
            else:
                vote = elector.next_vote(self.vote_rounds[-1])
            votes[vote] += 1

        self.vote_rounds.append(votes)
        self.rounds += 1
        return votes

    def run_elections(self):
        '''
        Run an entire election.
        '''

        winner = None

        while winner is None and self.rounds < self.max_rounds:
            election_results = self.vote()
            for result, votes in election_results.items():
                if votes/self.elector_count >= self.fraction_required:
                    winner = result

        # Maximum rounds reached, pick biggest vote-getter:
        if winner is None and self.rounds >= self.max_rounds:
            max_votes = 0
            max_option = None
            election_results = self.vote()
            for result, votes in election_results.items():
                if votes > max_votes:
                    max_option = result
                    max_votes = votes
        return winner






