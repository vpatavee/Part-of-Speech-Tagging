import json
import sys
import re
def count_word(reviews, labels, set_of_labels, how_token = 'standard' ):
    count = {}
    df = {}
    total = [0] * len(set_of_labels)
    for i,review in enumerate(reviews):
        class_num = set_of_labels.index(labels[i])
        tokens = tokenization(review, how_token)
        for token in tokens:
            if token not in count:
                count[token] = [0] * len(set_of_labels)
            count[token][class_num] += 1
            total[class_num] += 1
        set_of_tokens = set(tokens)
        for token in set_of_tokens:
            if token not in df:
                df[token] = 0
            df[token] += 1
    return count, total, df
                
def make_prob(count, total = [], how_smooth = 'add_one', param = 0):
    prob = {}
    num_token = len(count)
    if how_smooth == 'add_one':
        for token in count:
            prob[token] = [ (n + 1.0) / (total[i] + num_token) for i, n  in enumerate(count[token])]     
    elif how_smooth == 'JM':
        num_words_total = sum([sum(count[token]) for token in count])
        for token in count:
            prob_jm = sum(count[token]) / float(num_words_total)
            #print prob_jm
            prob[token] = [ param * (float(n) / total[i]) + (1 - param) * prob_jm for i, n  in enumerate(count[token])]   
        
    return prob

def make_prior_prob(labels, set_of_labels):
    prior_prob = [0] * len(set_of_labels)
    for label in labels:
        prior_prob[set_of_labels.index(label)] += 1.0
    return [n/len(labels) for n in prior_prob]            
     
def tokenization(review, how_token):
    if how_token == 'standard':
        return review.split()
    elif how_token == 'remove_punc':
        tokens = review.split()
        #return [token.strip('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~') for token in tokens]
        #return [token.strip('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~') if token.strip('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~') != '' else token for token in tokens]
        return re.findall("\w+", review)
        
        
def count_with_df(count, df, min_percent, max_percent):
    max_df = max([df[token] for token in df])
    max_df_token = [token for token in df if df[token] > max_percent * max_df]
    min_df_token = [token for token in df if df[token] < min_percent * max_df]
    for token in min_df_token:
        count.pop(token)
    for token in max_df_token:
        count.pop(token)

    

if __name__ == "__main__":

    reviews = []
    labels_1 = []
    labels_2 = []

    with open(sys.argv[1], 'r') as f:
        for line in f:
            reviews.append(line.split(" ",3)[3].strip())
            labels_1.append(line.split(" ",3)[1].strip())
            labels_2.append(line.split(" ",3)[2].strip())
            
    count_1, total_1, df1 = count_word(reviews, labels_1, ['Fake', 'True'], how_token = 'remove_punc')
    count_with_df(count_1, df1, min_percent = 0, max_percent = 0.5)
    prob_1 = make_prob(count_1, total_1)
    prior_prob_1 = make_prior_prob(labels_1, ['Fake', 'True'])

    count_2, total_2, df2 = count_word(reviews, labels_2, ['Neg', 'Pos'], how_token = 'remove_punc')
    count_with_df(count_2, df2, min_percent = 0, max_percent = 0.5)
    prob_2 = make_prob(count_2, total_2)
    prior_prob_2 = make_prior_prob(labels_2, ['Neg', 'Pos'])

    with open('nbmodel.txt', 'w') as f:
        f.write(json.dumps({"prior_prob_1":prior_prob_1, "prob_1":prob_1, "prior_prob_2": prior_prob_2, "prob_2":prob_2}))


