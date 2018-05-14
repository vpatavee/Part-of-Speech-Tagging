import sys
import json
import math

path = sys.argv[1]
fh = open(path, 'r')
corpus = fh.readlines()

def print_dict(d,fh):
    res = ""
    for k1 in d:
        for k2 in d[k1]:
            res += k1 + " " + k2 + " " + str(d[k1][k2]) + " "
        res += '\n'
    fh.write(res)
    

#transition probability

trans_prob = dict()
counter = 0
state_prob = dict()

for line in corpus:
    tokens = list(line.decode('utf-8').split())
    
    pos = ["START"] + [token.rsplit('/',1)[1] for token in tokens] + ["END"]
    #pos = ["START"] + [token.rsplit('/',1)[1] for token in tokens] 
    
    for p in pos:
        if p in state_prob.keys():
            state_prob[p] +=1
        else:
            state_prob[p] = 1.0
    
    for i in range(len(pos)-1):
        if pos[i] in trans_prob:
            if pos[i+1] in trans_prob[pos[i]]:
                trans_prob[pos[i]][pos[i+1]] += 1
            else:
                trans_prob[pos[i]][pos[i+1]] = 1.0
        else:
            trans_prob[pos[i]] = dict()
            trans_prob[pos[i]][pos[i+1]] = 1.0

    counter +=1 
    
#smoothing transition probability



all_pos = trans_prob.keys() + ["END"]

for k1 in trans_prob:
    for pos in all_pos:
        if pos in trans_prob[k1].keys():
            trans_prob[k1][pos] += 1
        else:
            trans_prob[k1][pos] = 1
            
for key in trans_prob:
    total = sum(trans_prob[key].values())
    for key2 in trans_prob[key]:
        trans_prob[key][key2] =math.log(trans_prob[key][key2]/ total)

#Jelinek-Mercer smoothing
# total_ = sum([n[1] for n in state_prob.items()])
# for key in state_prob:
    # state_prob[key] =state_prob[key]/ total_
            
# for k1 in trans_prob:
    # for pos in all_pos:
        # if pos in trans_prob[k1].keys():
            # trans_prob[k1][pos] += 0
        # else:
            # trans_prob[k1][pos] = 0  

# lamb = 0.9
# for key in trans_prob:
    # total = sum(trans_prob[key].values())
    # for key2 in trans_prob[key]:
        # trans_prob[key][key2] =(lamb * trans_prob[key][key2]/ total) + (1-lamb) * state_prob[key2]




#emission probability
emi_prob = dict()
counter = 0


for line in corpus:
    tokens = list(line.decode('utf-8').split())
    
    pairs = [(token.rsplit('/',1)[0],token.rsplit('/',1)[1]) for token in tokens] 
    
    for pair in pairs:
        if pair[1] in emi_prob:
            if pair[0] in emi_prob[pair[1]]:
                emi_prob[pair[1]][pair[0]] += 1
            else:
                emi_prob[pair[1]][pair[0]] = 1.0
        else:
            emi_prob[pair[1]] = dict()
            emi_prob[pair[1]][pair[0]] = 1.0

    counter +=1 
    #if counter >5: break
    
for pos in emi_prob:
    total = sum(emi_prob[pos].values())
    for w in emi_prob[pos]:
        emi_prob[pos][w] = math.log(emi_prob[pos][w]/total)
        
#json.dump({"emi":emi_prob, "tran":trans_prob}, open("hmmmodel.txt",'w'))

json_data = json.dumps({"emi":emi_prob, "tran":trans_prob}, ensure_ascii=False)
with open("hmmmodel.txt",'w') as outfile:
    outfile.write(json_data.encode('utf8'))