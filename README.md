# Global Classroom: Indiana University and Higher School of Economics - Predictive text for Chuckchi

## Team Info
- Olga Bystorva
- Liliya Kazakova
- Daniil Larionov

## Project details
Our submission is located at chukchi/baseline_tokenizer
### Method TL;DR
Trigram language model with sentencepiece tokenization

### Requirements
tokenizers == 0.10.2

### Reproduction
0. (optional, if something isn't working) Recreate tokenizer pickle file using tokenizer.ipynb notebook
1. Train the model: ```python train_trigrams.py ../data/train.tsv model.dat```
2. Run predictions: ```python predict_trigrams.py model.dat < ../data/test/test.tsv > output.tsv```
3. Evalute predictions ```python ../evaluate.py ../data/test/test.tsv output.tsv ```

### Results
```
Characters: 37927
Tokens: 8374
Clicks: 13918
Clicks/Token: 1.6620491999044662
Clicks/Character: 0.36696812297307985
```
