import sys

poss_ = dict()
hist = dict()
with open(sys.argv[1], 'r') as f:
    for line in f.readlines():
        tokens = list(line.decode('utf-8').split())
        for token in tokens:
            word = token.rsplit('/',1)[0]
            pos = token.rsplit('/',1)[1]
            if word in hist:
                if pos in hist[word]:
                    hist[word][pos] +=1 
                else:
                    hist[word][pos] = 1.0
                   
            else:
                hist[word] = {pos:1.0}
                
            if pos in poss_:
                poss_[pos] += 1
            else:
                poss_[pos] = 1.0
           
most_freq = dict()
for vocab in hist:
    most_freq[vocab] = max(hist[vocab], key = hist[vocab].get)   
           
MOST_FREQ_POS = max(poss_, key = poss_.get)

#Tag
with open(sys.argv[2],'r') as f:
    res = ""
    for line in f.readlines():
        tokens = line.decode('utf-8').split()   
        poss = []
        for token in tokens:
            if token in most_freq:
                poss.append(most_freq[token])
            else:
                poss.append(MOST_FREQ_POS)
        
        for token, pos in zip(tokens,poss):
            res += token + '/' + pos + ' '
        res += '\n'    

with open("baseline.txt", 'w') as f:
    f.write(res.encode('utf-8'))