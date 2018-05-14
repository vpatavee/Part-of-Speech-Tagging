import sys

fh_train = open(sys.argv[1], 'r')
fh_tag = open(sys.argv[2],'r')
fh_write = open("baseline.txt", 'w')
MOST_FREQ_POS = ""
poss_ = dict()
hist = dict()
for line in fh_train.readlines():
    tokens = list(line.decode('utf-8').split())
    for token in tokens:
        word = token.rsplit('/',1)[0]
        pos = token.rsplit('/',1)[1]
        if word in hist.keys():
            if pos in hist[word].keys():
                hist[word][pos] +=1 
            else:
                hist[word][pos] = 1.0
                
        else:
            hist[word] = {pos:1.0}
            
        if pos in poss_.keys():
            poss_[pos] += 1
        else:
            poss_[pos] = 1


            
most_freq = dict()
for vocab in hist:
    max_occur =0
    max_pos = ""
    for pos in hist[vocab]:
        if hist[vocab][pos] > max_occur:
            
            max_occur = hist[vocab][pos]
            max_pos = pos
    most_freq[vocab] = max_pos   
        
#most freq pos
temp =0
for pos in poss_:
    if poss_[pos] > temp:
        temp = poss_[pos]
        MOST_FREQ_POS = pos
    
print MOST_FREQ_POS

# tag
res = ""
for line in fh_tag.readlines():
    tokens = line.decode('utf-8').split()
    
    poss = []
    for token in tokens:
        if token in most_freq.keys():
            poss.append(most_freq[token])
        else:
            poss.append(MOST_FREQ_POS)
    
    for token, pos in zip(tokens,poss):
        res += token + '/' + pos + ' '
    res += '\n'    

fh_write.write(res.encode('utf-8'))