# -*- coding: utf-8 -*-
import sys, pickle
import tokenizers
# This is the training data
training_file = sys.argv[1]
# This is the filename that we will save the model in
model_file = sys.argv[2]

with open('tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)

# This is a list of sentences in the training data
corpus = []

# Unigram counts = how often we see tokens, e.g. a frequency list
unigram_counts = {}
# Probability of the individual unigram
unigrams = {}
# How often we see word2 after word1 (e.g. 'house' after 'big')
bigram_counts = {}  # bigram_counts['big']['house'] = 1, bigram_counts['big']['dog'] = 1
# Probability of word2 after word1
bigrams = {}  # bigrams['big']['house'] 0.5, ...
# PHow often we see  word3 after word1_word2
trigram_counts = {}
# Probability of word3 after word1_word2
trigrams = {}

quadgram_counts = {}
quadgrams = {}

fivegram_counts = {}
fivegrams = {}

# Read in the examples from the training data
for line in open(training_file).readlines():
    # Each line in the training data is two columns
    # тыкгаткэта ивнин риӄукэтэ	ты>кгат>кэ>та ив>ни>н риӄукэ>тэ
    row = line.strip().split('\t')
    # The tokens are in the first column
    tokens = tokenizer.encode(row[0]).ids
    # Add the tokens to the list of sentences, with a beginning of sentence and an end of sentence marker
    corpus.append([0, 0, 0] + tokens + [0, 0, 0])

# Collect unigram counts
n_tokens = 0  # Number of tokens
# For each of the sentences in our corpus
for sent in corpus:
    # For each of the tokens in the sentence
    for token in sent:
        # If we haven't seen the token before:
        if token not in unigram_counts:
            # Initialise the token count to zero
            unigram_counts[token] = 0
        # Increment the count of that token
        unigram_counts[token] += 1
    # Increment the count of all the tokens
    n_tokens += 1
# Estimate unigram probabilities
# For each of the types we have seen 
for token in unigram_counts:
    # The probability is the frequency of the token divided by the total number of tokens
    unigrams[token] = unigram_counts[token] / n_tokens

# Collect bigram counts
# e.g. ['the', 'big', 'house'] 
# bigrams: (the, big) (big, house)
# For each of the sentences in the corpus
for sent in corpus:
    # For each number in the range of 0..length of sentence - 1
    for i in range(0, len(sent) - 1):
        # The first word is the word at i
        w1 = sent[i]
        # The second word is the word at i+1
        w2 = sent[i + 1]
        # If we haven't seen the first word before, initialise a new dictionary for the second word
        if w1 not in bigram_counts:
            bigram_counts[w1] = {}
        # If we haven't seen the second word before, initialise the count to 0
        if w2 not in bigram_counts[w1]:
            bigram_counts[w1][w2] = 0
        # Increment the count
        bigram_counts[w1][w2] += 1

n_bigrams = 0
# Estimate bigram probabilities
# For each of the first words
for token1 in bigram_counts:
    # If we haven't seen it before, initialise it
    if token1 not in bigrams:
        bigrams[token1] = {}
    # Find the total frequency of all of the words that can go after this word
    token_total = sum(bigram_counts[token1].values())
    # For each of the second parts of the bigram
    for token2 in bigram_counts[token1]:
        # If we haven't seen the  second part before, initialise it to 0
        if token2 not in bigrams[token1]:
            bigrams[token1][token2] = 0
            n_bigrams += 1
        # Calculate the probability
        bigrams[token1][token2] = bigram_counts[token1][token2] / token_total

# Collect trigram counts
# e.g. ['the', 'big', 'house', 'of']
# bigrams: (the, big, house) (big, house, of)
# For each of the sentences in the corpus
for sent in corpus:
    # For each number in the range of 0..length of sentence - 1
    for i in range(0, len(sent) - 2):
        # The first word is the word at i
        w1 = sent[i]
        # The second word is the word at i+1
        w2 = sent[i + 1]
        # If we haven't seen the first word before, initialise a new dictionary for the second word
        w3 = sent[i + 2]

        if w1 not in trigram_counts:
            trigram_counts[w1] = {}
        # If we haven't seen the second word before, initialise the count to 0
        if w2 not in trigram_counts[w1]:
            trigram_counts[w1][w2] = {}
        if w3 not in trigram_counts[w1][w2]:
            trigram_counts[w1][w2][w3] = 0
        # Increment the count
        trigram_counts[w1][w2][w3] += 1

# TRIGRAMS
n_trigrams = 0
# Estimate trigram probabilities
# For each of the first words
for token1 in trigram_counts:
    # If we haven't seen it before, initialise it
    if token1 not in trigrams:
        trigrams[token1] = {}
    # Find the total frequency of all of the words that can go after this word
    # token_total = sum(trigram_counts[token1].values())
    # For each of the second parts of the bigram
    for token2 in trigram_counts[token1]:
        # If we haven't seen the  second part before, initialise it to 0
        if token2 not in trigrams[token1]:
            trigrams[token1][token2] = {}
            n_trigrams += 1
        # Calculate the probability
        token2_total = sum(trigram_counts[token1][token2].values())

        for token3 in trigram_counts[token1][token2]:
            if token3 not in trigrams[token1][token2]:
                trigrams[token1][token2][token3] = 0
                n_trigrams += 1
            trigrams[token1][token2][token3] = trigram_counts[token1][token2][token3] / token2_total
            
# QuadGrams
for sent in corpus:
    # For each number in the range of 0..length of sentence - 3
    for i in range(0, len(sent) - 3):
        # The first word is the word at i
        w1 = sent[i]
        # The second word is the word at i+1
        w2 = sent[i + 1]
        # If we haven't seen the first word before, initialise a new dictionary for the second word
        w3 = sent[i + 2]
        w4 = sent[i + 3]

        if w1 not in quadgram_counts:
            quadgram_counts[w1] = {}
        # If we haven't seen the second word before, initialise the count to 0
        if w2 not in quadgram_counts[w1]:
            quadgram_counts[w1][w2] = {}
        if w3 not in quadgram_counts[w1][w2]:
            quadgram_counts[w1][w2][w3] = {}
        if w4 not in quadgram_counts[w1][w2][w3]:
            quadgram_counts[w1][w2][w3][w4] = 0
        # Increment the count
        quadgram_counts[w1][w2][w3][w4] += 1
        
# Quadgram probabilities
n_quadgrams = 0
# Estimate trigram probabilities
# For each of the first words
for token1 in quadgram_counts:
    # If we haven't seen it before, initialise it
    if token1 not in quadgrams:
        quadgrams[token1] = {}
    # Find the total frequency of all of the words that can go after this word
    # token_total = sum(trigram_counts[token1].values())
    # For each of the second parts of the bigram
    for token2 in quadgram_counts[token1]:
        # If we haven't seen the  second part before, initialise it to 0
        if token2 not in quadgrams[token1]:
            quadgrams[token1][token2] = {}
            
        
        for token3 in quadgram_counts[token1][token2]:
            if token3 not in quadgrams[token1][token2]:
                quadgrams[token1][token2][token3] = {}
                
            token3_total = sum(quadgram_counts[token1][token2][token3].values())
            
            for token4 in quadgram_counts[token1][token2][token3]:
                if token4 not in quadgrams[token1][token2][token3]:
                    quadgrams[token1][token2][token3][token4] = 0
                    n_quadgrams += 1
                    
                quadgrams[token1][token2][token3][token4] = quadgram_counts[token1][token2][token3][token4] / token3_total

# Write out model
mf = open(model_file, 'wb')
pickle.dump((unigrams, bigrams, trigrams, quadgrams), mf)
print('Written %d unigrams, %d bigrams, %d trigrams and %d quadgrams to %s.' % (len(unigrams.keys()),
                                                                      n_bigrams,
                                                                      n_trigrams,
                                                                      n_quadgrams,
                                                                      model_file))
