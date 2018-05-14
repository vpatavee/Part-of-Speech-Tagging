import sys
import operator

path_predict = sys.argv[1]
path_tagged = sys.argv[2]

fh_predict = open(path_predict, 'r')
fh_tagged = open(path_tagged, 'r')

predict = fh_predict.readlines()
tagged = fh_tagged .readlines()

if len(predict) != len(tagged): 
    print "File Error"
    exit()

res = dict()
count_all =0.0
count_wrong =0.0

for i in range(len(predict)):
    pre = predict[i].split()
    tag = tagged[i].split()
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
res = sorted(res.items(), key=operator.itemgetter(1))
print res + '\n'
print "number of wrong " + str(count_wrong)
print "accuracy =" + str(acc)

