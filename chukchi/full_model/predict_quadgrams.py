# -*- coding: utf-8 -*-
from __future__ import print_function
import sys, pickle

# This is the filename of the model file
model_file = sys.argv[1]
mf = open(model_file, 'rb')

with open('tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)

# Load the unigram and bigram probabilities from the model file
(unigrams, bigrams, trigrams, quadgrams) = pickle.load(mf, encoding='utf-8')

# Initialise the probability of the start of the sentence.
unigrams[0] = 0.0
bigrams[0][0] = 0.0
trigrams[0][0][0] = 0.0
# Hits is number of times we get a prediction right
hits = 0
# The number of tokens
n_tokens = 0
# For each of the lines in the input
for line in sys.stdin.readlines():
    # Split into two columns
    row = line.strip().split('\t')
    # Our tokens are in column one, split by space
    tokens = tokenizer.encode(row[0]).ids
    # The test tokens are the beginning of sentence symbol + the list of tokens
    tst_tokens = [0, 0, 0] + tokens
    # Increment the number of tokens by the length of the list containing the tokens
    n_tokens += len(tokens)

    # This is our output
    output = []
    # For each of the tokens in the "tst_tokens" list (e.g. the list + the beginning of sentence symbol)
    for i in range(len(tst_tokens) - 3):
        up = 0.0  # Unigram probability
        bp = 0.0  # Bigram probability
        tp = 0.0  # Trigram probability
        qp = 0.0  # quads probability
        first = tst_tokens[i]  # First token in bigram
        second = tst_tokens[i + 1]  # Second token in trigram
        third = tst_tokens[i + 2]
        fourth = tst_tokens[i + 3]
        # If we find the first token in the bigrams dict
        if first in quadgrams:
            if second in quadgrams[first]:
                if third in quadgrams[first][second]:
                    # ==========================================================
                    # Quadgrams
                    # ==========================================================
                    # We get the best prediction for what token should come next
                    pred = max(quadgrams[first][second][third], key=quadgrams[first][second][third].get)
                    # If it matches with what the next token really is
                    if pred == fourth:
                        # We add this whole token to the output
                        # e.g. a single click on a prediction
                        output.append(tokenizer.decode([pred]))
                        # Increment the number of hits by 1
                        hits += 1
                    else:
                        # Otherwise we add each individual character to the output
                        # e.g. writing out each of the individual clicks
                        output += [c for c in tokenizer.decode([fourth])]
                elif second in trigrams and third in trigrams[second]:
                    # ==========================================================
                    # Backoff to trigrams
                    # ==========================================================
                    # Find the highest scoring unigram
                    pred = max(trigrams[second][third], key=trigrams[second][third].get)
                    # If the prediction is right
                    if pred == fourth:
                        # Append to output
                        output.append(tokenizer.decode([pred]))
                        hits += 1
                    else:
                        # Otherwise append each individual character
                        output += [c for c in tokenizer.decode([fourth])]
            elif third in bigrams:
                # ==========================================================
                # Backoff to unigrams
                # ==========================================================
                # Find the highest scoring unigram
                pred = max(bigrams[third], key=bigrams[third].get)
                # If the prediction is right
                if pred == fourth:
                    # Append to output
                    output.append(tokenizer.decode([pred]))
                    hits += 1
                else:
                    # Otherwise append each individual character
                    output += [c for c in tokenizer.decode([fourth])]
        else:
            # ==========================================================
            # Backoff to unigrams
            # ==========================================================
            # Find the highest scoring unigram
            pred = max(unigrams, key=unigrams.get)
            # If the prediction is right
            if pred == fourth:
                # Append to output
                output.append(tokenizer.decode([pred]))
                hits += 1
            else:
                # Otherwise append each individual character
                output += [c for c in tokenizer.decode([fourth])]
        # Finally append a space symbol
        if tokenizer.id_to_token(second).startswith('▁'):
            output.append('_')
    # break
    # Print out our input and the predicted sequence of keypresses
    print('%s\t%s' % (row[0], ' '.join(output)))

print('Hits:', hits, '; Tokens:', n_tokens, file=sys.stderr)
