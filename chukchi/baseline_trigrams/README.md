# Baseline system

This is a simple next-word prediction system using bigram probabilities. For each word in the input it 
tries to predict the next word and falls back to predicting the most frequent unigram.

You can train the system by using:

```bash
$ python3 train.py ../data/train.tsv model.dat
Written 33724 unigrams and 107835 bigrams to model.dat.
```

And then you can run it using:

```bash
$ python3 predict.py model.dat < ../data/test/test.tsv > output.tsv
```

RESULTS 

```bash
$ python3 ../evaluate.py ../data/test/test.tsv output.tsv 
Characters: 37927
Tokens: 8374
Clicks: 30340
Clicks/Token: 3.6231191784093624
Clicks/Character: 0.7999578136947294
```

Results with concatenation dev + train
```bash
Characters: 37927
Tokens: 8374
Clicks: 30363
Clicks/Token: 3.6258657750179126
Clicks/Character: 0.800564241832995
```
