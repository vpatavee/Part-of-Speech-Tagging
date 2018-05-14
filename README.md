# Part of Speech Tagging with Hidden Markov Model
By Patavee Meemeng

This code is developed for educational propose. I do experiment on many variations of HMM. The results are benchmarked with [Scikit-learn HMM](http://scikit-learn.sourceforge.net/stable/modules/hmm.html).

**baseline.py**

This code is used to calculate the baseline accuracy. The baseline tagger gives the most common tag for each word. The baseline accuracy of this corpus is 0.8399 for English and 0.8358 for Chinese


**hmmlearn.py**

* Basic HMM implementation as described in [Speech and Language Processing (Jurafsky & Martin)](https://web.stanford.edu/~jurafsky/slp3/10.pdf) This yield the accuracy of 0.8803 for English and 0.8629 for Chinese.

**hmmdecode.py**

**eval.py**

This code is invoked in the following way:
> python baseline.py /predicted_file /key_file

This code can be called from other program by:
>eval(/predicted_file, /key_file)
It will return the following 
* accuracy 
* part-of-speeach and number of incorrect predictions as dictionary