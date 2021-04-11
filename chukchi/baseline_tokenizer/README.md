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
$ python3 predict.py model.dat < ../data/dev.tsv > output.tsv
```

BIGRAMS RESULT

```bash
$ python3 ../evaluate.py ../data/dev.tsv output.tsv 
Characters: 37927
Tokens: 8374
Clicks: 36240
Clicks/Token: 4.327680917124432
Clicks/Character: 0.9555198143802568

```

TRIGRAMS RESULT
```bash
$ python3 ../evaluate.py ../data/dev.tsv output.tsv 
Characters: 37927
Tokens: 8374
Clicks: 13878
Clicks/Token: 1.6572725101504657
Clicks/Character: 0.3659134653413136
```

TRIGRAMS RESULT ON DEV+TRAIN SET
```bash
$ python3 ../evaluate.py ../data/dev.tsv output.tsv 
Characters: 37927
Tokens: 8374
Clicks: 13918
Clicks/Token: 1.6620491999044662
Clicks/Character: 0.36696812297307985
```