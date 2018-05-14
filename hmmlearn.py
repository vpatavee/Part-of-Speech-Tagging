import sys
import json
import math

def count_transition(corpus):
    trans_prob = dict()
    state_prob = dict()
    for line in corpus:
        tokens = list(line.decode('utf-8').split())      
        pos = ["START"] + [token.rsplit('/',1)[1] for token in tokens] + ["END"]
        
        for p in pos:
            if p in state_prob:
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
    
    all_pos = trans_prob.keys() + ["END"]
            
    return trans_prob, state_prob, all_pos

def count_emission(corpus):
    emi_prob = dict()
    for line in corpus:
        tokens = list(line.decode('utf-8').split())
        pairs = [(token.rsplit('/',1)[0],token.rsplit('/',1)[1]) for token in tokens] 
        all_vocab = set()
        for pair in pairs:
            all_vocab.add(pair[0])
            if pair[1] in emi_prob:
                if pair[0] in emi_prob[pair[1]]:
                    emi_prob[pair[1]][pair[0]] += 1
                else:
                    emi_prob[pair[1]][pair[0]] = 1.0
            else:
                emi_prob[pair[1]] = dict()
                emi_prob[pair[1]][pair[0]] = 1.0
                
    return emi_prob, all_vocab

    
def make_prob(counting, all_keys = None, how = None, log = True, param = None, state_prob = None):
    probability = counting.copy()
    if how == "add-1":
        for k1 in counting:
            for pos in all_keys:
                if pos in counting[k1]:
                    probability[k1][pos] += 1
                else:
                    probability[k1][pos] = 1
                 
    elif how == "Jelinek-Mercer":
        total_ = sum([n[1] for n in state_prob.items()])
        for key in state_prob:
            state_prob[key] =state_prob[key]/ total_
                    
        for k1 in probability:
            for pos in all_pos:
                if pos in probability[k1].keys():
                    probability[k1][pos] += 0
                else:
                    probability[k1][pos] = 0  

        for key in probability:
            total = sum(probability[key].values())
            for key2 in probability[key]:
                probability[key][key2] =math.log((param * probability[key][key2]/ total) + (1-param) * state_prob[key2])
                
        return probability
    
    for key in probability:
        total = sum(probability[key].values())
        for key2 in probability[key]:
            if log:
                probability[key][key2] =math.log(counting[key][key2]/ total)  
            else:
                probability[key][key2] =probability[key][key2]/ total

    return probability        


if __name__ == "__main__":    

    with open(sys.argv[1], 'r') as f:
        corpus = f.readlines()    
        
    trans_prob, state_prob, all_pos = count_transition(corpus)
    trans_prob = make_prob(trans_prob, all_pos, how = "Jelinek-Mercer", param = 0.95, state_prob = state_prob)
    #trans_prob = make_prob(trans_prob, all_pos, how = "add-1")
    emi_prob, all_vocab = count_emission(corpus)
    emi_prob = make_prob(emi_prob)

    with open("hmmmodel.txt",'w') as f:
        json.dump({"emi":emi_prob, "tran":trans_prob}, f, encoding="utf-8")