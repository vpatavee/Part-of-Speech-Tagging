import sys
import json
import numpy as np
   

def viterbi(words, emi_prob, trans_prob, all_vocab,oc, isLog = True):
    
    num_words = len(words)
    states = trans_prob.keys()
    states.remove("START")
    num_state = len(states)
    t = np.zeros((num_state, num_words ), dtype = list)

    #start 
    for i in range(num_state):
        if words[0] in all_vocab:
            if words[0] in emi_prob[states[i]]:
                if isLog:
                    t[i,0] = [trans_prob['START'][states[i]] + emi_prob[states[i]][words[0]], "START"]
                else:
                    t[i,0] = [trans_prob['START'][states[i]] * emi_prob[states[i]][words[0]], "START"]
            
            else:
                if isLog:
                    t[i,0] = [float('-inf'),-1]

                else:
                    t[i,0] = [0.0,-1]
        else:
            if states[i] in oc:
                t[i,0] = [trans_prob['START'][states[i]], "START"]

            else:
                t[i,0] = [trans_prob['START'][states[i]]-2, "START"]

    #iterate
    for i in range(1,num_words):

        if words[i] in all_vocab:
            for j in range(num_state):
                if words[i] in emi_prob[states[j]]:
                    if isLog:
                        candidates = [t[k,i-1][0] + trans_prob[states[k]][states[j]] for k in range(num_state) ]
                        id = np.argmax(candidates)      
                        t[j,i] = [candidates[id] + emi_prob[states[j]][words[i]], id] 
                    else:
                        candidates = [t[k,i-1][0] * trans_prob[states[k]][states[j]] for k in range(num_state)]
                        id = np.argmax(candidates)      
                        t[j,i] = [candidates[id] * emi_prob[states[j]][words[i]], id]                              
                else:
                    if isLog:
                        t[j,i] = [float('-inf'),-1]                   
                    else:
                        t[j,i] = [0.0,-1]
        else:
            for j in range(num_state):
                if isLog:    
                    candidates = [t[k,i-1][0] + trans_prob[states[k]][states[j]]  if states[k] in oc else t[k,i-1][0] + trans_prob[states[k]][states[j]]-2 for k in range(num_state)]
                else:
                    candidates = [t[k,i-1][0] * trans_prob[states[k]][states[j]] for k in range(num_state)]

                id = np.argmax(candidates)      
                t[j,i] = [candidates[id], id]              

    #end
    if isLog:
        end_prob = [ t[i,num_words-1][0] + trans_prob[states[i]]['END'] for i in range(num_state)]
    else:
        end_prob = [ t[i,num_words-1][0] * trans_prob[states[i]]['END'] for i in range(num_state)]
    
    res = [np.argmax(end_prob)]
    for i in range(num_words-1,0,-1):
        res = [t[res[0],i][1]] + res
    tagged = [states[int(id)] for id in res]   
   
    return tagged    
    
    
if __name__ == "__main__":

    param = json.loads(open("./hmmmodel.txt", 'r').read().decode('utf-8'))
    emi_prob = param['emi']
    trans_prob = param['tran']
    all_vocab = set([vocab for pos in emi_prob for vocab in emi_prob[pos]])   
    if 'open_class' in param:
        oc = [ l for l in param['open_class']]
    else:
        oc = []
        
    res = ""
    with open(sys.argv[1], 'r') as f:
        for line in f.readlines():
            tokens = line.decode('utf-8').split()
            poss = viterbi(tokens, emi_prob, trans_prob, all_vocab,oc)

            for token, pos in zip(tokens,poss):
                res += token + '/' + pos + ' '
            res += '\n'

    with open("hmmoutput.txt",'w')  as f:        
        f.write(res.encode('utf-8'))
