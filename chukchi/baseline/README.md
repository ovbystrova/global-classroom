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

Use the provided evaluation script to evaluate the system:

```bash
$ python3 ../evaluate.py ../data/dev.tsv output.tsv 
Characters: 37897
Tokens: 8788
Clicks: 37754
Clicks/Token: 4.2960855712335
Clicks/Character: 0.9962266142438716
```

Results with concatenation dev + train
```bash
$ python3 ../evaluate.py ../data/dev.tsv output.tsv 
Characters: 37927
Tokens: 8374
Clicks: 37768
Clicks/Token: 4.510150465727251
Clicks/Character: 0.995807735913729
```