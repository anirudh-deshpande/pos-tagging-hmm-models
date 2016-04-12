# pos-tagging-hmm-models
Parts of speech tagging of Catalan corpus using Hidden Markov Models. 

hmmmodel.py takes catalan_corpus_train_tagged.txt as input and builds a model hmmmodel.txt.

hmmdecode.py takes hmmmodel.txt as input to read the model, and also takes catalan_corpus_dev_raw.txt and performs POS tagging on this content.

The program executes with an accuracy of 92%.
