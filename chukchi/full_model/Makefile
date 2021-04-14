all: model.dat output.tsv
	python ../evaluate.py ../data/test/test.tsv output.tsv

model.dat:
	python train_fivegrams.py ../data/train_dev.tsv model.dat

output.tsv:
	python predict_fivegrams.py model.dat < ../data/test/test.tsv > output.tsv

clean:
	rm model.dat output.tsv
