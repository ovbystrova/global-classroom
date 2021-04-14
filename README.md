# Global Classroom: Indiana University and Higher School of Economics - Predictive text for Chuckchi

## Team Info
- Olga Bystorva
- Liliya Kazakova
- Daniil Larionov

## Project details
Our submission is located at chukchi/full_model
### Method TL;DR
5-gram language model with sentencepiece tokenization

### Requirements
```tokenizers == 0.10.2```

### Reproduction
0. cd chuckchi/full_model
1. (optional, if something isn't working) Recreate tokenizer pickle file using tokenizer.ipynb notebook
2. make clean
3. make all`

### Results
```
Characters: 37927
Tokens: 8374
Clicks: 35386
Clicks/Token: 4.225698590876522
Clicks/Character: 0.9330028739420466
```
