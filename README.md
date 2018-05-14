# Part of Speech Tagging with Hidden Markov Model
By Patavee Meemeng

This code is developed for educational propose. I do experiment on many variations of HMM. The results are benchmarked with [Scikit-learn HMM](http://scikit-learn.sourceforge.net/stable/modules/hmm.html).

**baseline.py**

This code is used to calculate the baseline accuracy. The baseline tagger gives the most common tag for each word. The baseline accuracy of this corpus is 0.8399 for English and 0.8358 for Chinese


**hmmlearn.py**

The program will learn a hidden Markov model from the training data. The learning program will be invoked in the following way:

> python hmmlearn.py /input


The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt. 

The program is designed to support any languages, so each word is treated as a symbol. In other words, the program will not take word shape like whether it starts with capital, whether it contains cardinal number, in to account.

The variations are implemented and the results are recorded as follows;

* Basic HMM implementation as described in [Speech and Language Processing (Jurafsky & Martin)](https://web.stanford.edu/~jurafsky/slp3/10.pdf) This yield the accuracy of 0.8803 for English and 0.8629 for Chinese.
* Implement [Jelinek-Mercer smoothing](https://nlp.stanford.edu/~wcmac/papers/20050421-smoothing-tutorial.pdf)
* Implement [Good-Turing smoothing](https://nlp.stanford.edu/~wcmac/papers/20050421-smoothing-tutorial.pdf)
* Implement constraint for unknown words that limits their potential tags to those labels with the most unique types 


**hmmdecode.py**
The tagging program will be invoked in the following way:

> python hmmdecode.py /path/to/input

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.


**eval.py**

This code is invoked in the following way:
> python baseline.py /predicted_file /key_file

This code can be called from other program by:
>eval(/predicted_file, /key_file)

It will return the following 
* accuracy 
* part-of-speeach and number of incorrect predictions as dictionary