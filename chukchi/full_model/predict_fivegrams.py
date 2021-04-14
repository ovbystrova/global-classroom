# -*- coding: utf-8 -*-
from __future__ import print_function
import sys, pickle

# This is the filename of the model file
model_file = sys.argv[1]
mf = open(model_file, 'rb')

with open('tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)

# Load the unigram and bigram probabilities from the model file
(unigrams, bigrams, trigrams, quadgrams, fivegrams) = pickle.load(mf, encoding='utf-8')

def predict_unigram(target_word):
    pred = max(unigrams, key=unigrams.get)
    # If the prediction is right
    if pred == target_word:
        # Append to output
        return [tokenizer.decode([pred])]
        hits += 1
    else:
        # Otherwise append each individual character
        return [c for c in tokenizer.decode([target_word])]
    
def predict_bigram(token1, target_word):
    # Find the highest scoring unigram
    pred = max(bigrams[token1], key=bigrams[token1].get)
    # If the prediction is right
    if pred == target_word:
        # Append to output
        return [tokenizer.decode([pred])]
        hits += 1
    else:
        # Otherwise append each individual character
        return [c for c in tokenizer.decode([target_word])]
    
def predict_trigram(token1, token2, target_word):
    pred = max(trigrams[token1][token2], key=trigrams[token1][token2].get)
    # If the prediction is right
    if pred == target_word:
        # Append to output
        return [tokenizer.decode([pred])]
        hits += 1
    else:
        # Otherwise append each individual character
        return [c for c in tokenizer.decode([target_word])]
    
def predict_quadgram(token1, token2, token3, target_word):
    # We get the best prediction for what token should come next
    pred = max(quadgrams[token1][token2][token3], key=quadgrams[token1][token2][token3].get)
    # If it matches with what the next token really is
    if pred == target_word:
        # We add this whole token to the output
        # e.g. a single click on a prediction
        return [tokenizer.decode([pred])]
        # Increment the number of hits by 1
        hits += 1
    else:
        # Otherwise we add each individual character to the output
        # e.g. writing out each of the individual clicks
        return [c for c in tokenizer.decode([target_word])]
    
def predict_fivegram(token1, token2, token3, token4, target_word):
    pred = max(fivegrams[token1][token2][token3][token4], key=fivegrams[token1][token2][token3][token4].get)
    # If it matches with what the next token really is
    if pred == target_word:
        # We add this whole token to the output
        # e.g. a single click on a prediction
        return [tokenizer.decode([pred])]
        # Increment the number of hits by 1
        hits += 1
    else:
        # Otherwise we add each individual character to the output
        # e.g. writing out each of the individual clicks
        return [c for c in tokenizer.decode([target_word])]

# Initialise the probability of the start of the sentence.
unigrams[0] = 0.0
bigrams[0][0] = 0.0
trigrams[0][0][0] = 0.0
quadgrams[0][0][0][0] = 0.0
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
    tst_tokens = [0, 0, 0, 0] + tokens
    # Increment the number of tokens by the length of the list containing the tokens
    n_tokens += len(tokens)

    # This is our output
    output = []
    # For each of the tokens in the "tst_tokens" list (e.g. the list + the beginning of sentence symbol)
    for i in range(len(tst_tokens) - 4):
        first = tst_tokens[i]  # First token in bigram
        second = tst_tokens[i + 1]  # Second token in trigram
        third = tst_tokens[i + 2]
        fourth = tst_tokens[i + 3]
        fifth = tst_tokens[i + 4]
        # If we find the first token in the bigrams dict
        if first in fivegrams:
            if second in fivegrams[first]:
                if third in fivegrams[first][second]:
                    if fourth in fivegrams[first][second][third]:
                        # ==========================================================
                        # Five-grams
                        # ==========================================================
                        output += predict_fivegram(first, second, third, fourth, fifth)
                    elif second in quadgrams and third in quadgrams[second] and fourth in quadgrams[second][third]:
                        # ==========================================================
                        # Quadgrams
                        # ==========================================================
                        output += predict_quadgram(second, third, fourth, fifth)
                    elif third in trigrams and fourth in trigrams[third]:
                        # ==========================================================
                        # Trigrams
                        # ==========================================================
                        output += predict_trigram(third, fourth, fifth)
                    elif fourth in bigrams:
                        # ==========================================================
                        # Bigrams
                        # ==========================================================
                        output += predict_bigram(fourth, fifth)
                    else:
                        # ==========================================================
                        # Unigrams
                        # ==========================================================
                        output += predict_unigram(fifth)
                elif second in quadgrams and third in quadgrams[second] and fourth in quadgrams[second][third]:
                    # ==========================================================
                    # Quadgrams
                    # ==========================================================
                    output += predict_quadgram(second, third, fourth, fifth)
                    
                elif third in trigrams and fourth in trigrams[third]:
                    # ==========================================================
                    # Backoff to trigrams
                    # ==========================================================
                    
                    output += predict_trigram(third, fourth, fifth)
                    
                elif fourth in bigrams:
                    # ==========================================================
                    # Backoff to bigrams
                    # ==========================================================
                    output += predict_bigram(fourth, fifth)
                        
                else:
                    # ==========================================================
                    # Backoff to unigrams
                    # ==========================================================
                    output += predict_unigram(fifth)
                 
            elif fourth in bigrams:
                # ==========================================================
                # Backoff to bigrams
                # ==========================================================
                output += predict_bigram(fourth, fifth)
            else:
                # ==========================================================
                # Backoff to unigrams
                # ==========================================================
                output += predict_unigram(fifth)
        else:
            # ==========================================================
            # Backoff to unigrams
            # ==========================================================
            output += predict_unigram(fifth)
        # Finally append a space symbol
        if tokenizer.id_to_token(second).startswith('▁'):
            output.append('_')
    # break
    # Print out our input and the predicted sequence of keypresses
    print('%s\t%s' % (row[0], ' '.join(output)))

print('Hits:', hits, '; Tokens:', n_tokens, file=sys.stderr)
