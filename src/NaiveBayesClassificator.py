import math
from collections import Counter

class Classifier:
    """
    Object for performing naive bayesian classification.
    """
    def __init__(self, outcomes):
        """Take a list of outcomes as strings, construct classifier."""
        # Prepare outcome object list
        self.outcomes = { }
        self.tokens_count = {}
        self.total_count = 0
        for outcome in outcomes:
            self.outcomes[outcome] = Outcome()

    def add_training_example(self, outcome, tokens):
        """Take an outcome and a list of tokens and update the outcome object."""
        self.outcomes[outcome].add_training_example(tokens)
        self.total_count += self.outcomes[outcome].count
        self.tokens_count = dict(Counter(self.tokens_count) + Counter(self.outcomes[outcome].token_counts))
    
    def probability_outcome(self, outcome):
        """Give P(O) for outcome O."""
        return float(self.outcomes[outcome].count) / sum([outcome_obj.count for outcome_name, outcome_obj in self.outcomes.iteritems()])

    def probability_tokens(self, tokens):
        """Give P(T1 & T2 & ... & Tn) for tokens Ti."""
        return sum([outcome_obj.probability_tokens_given_outcome(tokens) for outcome_name, outcome_obj in self.outcomes.iteritems()])
    
    def probability_outcome_given_token(self, token, outcome):
        """Give P(O | T) for outcome O and token T."""
        # Find the total probability of the token and check it's not zero
        token_probability = (sum([self.outcomes[other_outcome].probability_token_given_outcome(token) * self.probability_outcome(other_outcome) for other_outcome in self.outcomes.keys()]))
        if token_probability <= 0.0000001:
            return 0.0
        # Bayes formula
        return (
            self.outcomes[outcome].probability_token_given_outcome(token) * self.probability_outcome(outcome) / token_probability)

    def probability_outcome_given_tokens_old(self, tokens, outcome):
        """Give P(O | T1 & T2 & ... & Tn) for outcome O and tokens Ti."""
        # For each token, calculate the probability of the outcome
        probabilities = [self.probability_outcome_given_token(token, outcome) for token in tokens]
        # Combine the probabilities using sigmoid to avoid floating point underflow,
        # and ignore prboabilities of 1 or 0 which cause the answer to be undefined
        exponent = sum([math.log(1 - p) - math.log(p) for p in probabilities if p != 0 and p != 1])
        return 1.0 / (1 + math.exp(exponent))

    def probability_outcome_given_tokens(self, tokens, outcome):
        probabilities = [self.probability_outcome_given_token(token, outcome) for token in tokens]
        probability_outcome = self.outcomes[outcome].count * 1.0 / self.total_count 
        single_pro = 1.0
        situ_pro = 1.0
        flag = 0
        totol_tokens = sum([self.tokens_count[t] for t in self.tokens_count])
        for token in tokens:
            single_pro *= self.tokens_count[token] * 1.0 / totol_tokens
            if token in self.outcomes[outcome].token_prob:
                flag = 1
                situ_pro *= self.outcomes[outcome].token_prob[token]
        return abs(situ_pro * flag * probability_outcome / single_pro - 1)

    def classify_tokens(self, tokens):
        """Find the probability of each outcome given a set of tokens."""
        outcome_probabilities = dict([(outcome, abs(self.probability_outcome_given_tokens(tokens, outcome)-1)) for outcome in self.outcomes.keys()])
        return outcome_probabilities

    def most_likely_outcome(self, tokens):
        """Find the most likely outcome given a set of tokens."""
        return min(self.outcomes.keys(), key=lambda outcome: self.probability_outcome_given_tokens(tokens, outcome))


class Outcome:
    """
    Object for representing an outcome and the tokens present when that
    outcome occurs.
    """
    def __init__(self):
        """Construct empty outcome object."""
        self.token_counts = {}
        self.count = 0
        self.token_prob = {}

    def add_training_example(self, tokens):
        """Take a token and increment the count for that token."""
        # Increment the outcome count
        self.count += 1
        tmp_count = 0
        # Increment the count of every token
        for token in tokens:
            if self.token_counts.has_key(token):
                self.token_counts[token] += 1
            else:
                self.token_counts.setdefault(token,1)
            tmp_count += self.token_counts[token]
        for token in self.token_counts:
            if self.token_prob.has_key(token):
                continue
            else:
                self.token_prob[token] = (self.token_counts[token] + 0.0) / tmp_count
    
    def probability_token_given_outcome(self, token):
        """Give P(T | O) for token T and this outcome O."""
        if self.token_counts.has_key(token):
            return float(self.token_counts[token]) / self.count
        else:
            return 0.0
