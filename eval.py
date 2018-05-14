import sys
def eval(fname1, fname2):
    with open(fname1, 'r') as f:
        predict = f.readlines()
        
    with open(fname2, 'r') as f:
        tagged = f.readlines()

    if len(predict) != len(tagged): 
        print "File Error"
        exit()

    res = dict()
    count_all = 0.0
    count_wrong = 0.0

    for line in zip(predict,tagged):
        pre = line[0].split()
        tag = line[1].split()
        for p, t in zip(pre,tag):
            count_all += 1
            if p!=t:
                count_wrong +=1
                mismatched = p.rsplit('/',1)[1] + '/' + t.rsplit('/',1)[1]
                if mismatched in res.keys():
                    res[mismatched] += 1
                else:
                    res[mismatched] =1
             
    acc = (count_all-count_wrong)/count_all
    return acc, res
 
if __name__ == "__main__":
    acc = eval(sys.argv[1], sys.argv[2])[0]
    print "accuracy = {:.4f}".format(acc)