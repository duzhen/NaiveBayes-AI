import sys
import math

training = sys.argv[1]
testing = sys.argv[2]
futureLine = 0
futureWords = 0
future = dict()
wise = dict()
wiseLine = 0
wiseWords = 0
allKey = dict()

with open(training) as f:
    content = f.readlines()
    content = [x.strip() for x in content]
    for c in content:
        line = c.split('\t')
        if line[0] == 'future':
            futureLine+=1
            for word in line[1].split(' '):
                if word in future.keys():
                    future[word] = future[word]+1
                else:
                    future[word] = 1
                
                futureWords+=1
                if word in allKey.keys():
                    allKey[word] = allKey[word]+1
                else:
                    allKey[word] = 1
        elif line[0] == 'wise':
            wiseLine+=1
            for word in line[1].split(' '):
                if word in wise.keys():
                    wise[word] = wise[word]+1
                else:
                    wise[word] = 1
                
                wiseWords+=1
                if word in allKey.keys():
                    allKey[word] = allKey[word]+1
                else:
                    allKey[word] = 1
print('A')
p_future = futureLine/(futureLine+wiseLine)
p_wise = wiseLine/(futureLine+wiseLine)
print(p_future, p_wise)
print('P(future)={}/{}'.format(futureLine, futureLine+wiseLine))
print('P(wise)={}/{}'.format(wiseLine, futureLine+wiseLine))
if 'tomorrow' in future.keys():
    print('P(tomorrow|future)={}/{}'.format(future['tomorrow'],futureWords))
else:
    print('P(tomorrow|future)={}/{}'.format(0,futureWords))

if 'tomorrow' in wise.keys():
    print('P(tomorrow|wise)={}/{}'.format(wise['tomorrow'],wiseWords))
else:
    print('P(tomorrow|wise)={}/{}'.format(0,wiseWords))

if 'wisdom' in future.keys():
    print('P(wisdom|future)={}/{}'.format(future['wisdom'],futureWords))
else:
    print('P(wisdom|future)={}/{}'.format(0,futureWords))
if 'wisdom' in wise.keys():
    print('P(wisdom|wise)={}/{}'.format(wise['wisdom'],wiseWords))
else:
    print('P(wisdom|wise)={}/{}'.format(0,wiseWords))

print('B')
uniqueWords = len(allKey)
# print('P(future)={}/{}'.format(futureLine, futureLine+wiseLine))
# print('P(wise)={}/{}'.format(wiseLine, futureLine+wiseLine))
if 'tomorrow' in future.keys():
    print('P(tomorrow|future)={}/{}'.format(future['tomorrow']+0.5,futureWords+0.5*uniqueWords))
else:
    print('P(tomorrow|future)={}/{}'.format(0.5,futureWords+0.5*uniqueWords))

if 'tomorrow' in wise.keys():
    print('P(tomorrow|wise)={}/{}'.format(wise['tomorrow']+0.5,wiseWords+0.5*uniqueWords))
else:
    print('P(tomorrow|wise)={}/{}'.format(0.5,wiseWords+0.5*uniqueWords))

if 'wisdom' in future.keys():
    print('P(wisdom|future)={}/{}'.format(future['wisdom']+0.5,futureWords+0.5*uniqueWords))
else:
    print('P(wisdom|future)={}/{}'.format(0.5,futureWords+0.5*uniqueWords))
if 'wisdom' in wise.keys():
    print('P(wisdom|wise)={}/{}'.format(wise['wisdom']+0.5,wiseWords+0.5*uniqueWords))
else:
    print('P(wisdom|wise)={}/{}'.format(0.5,wiseWords+0.5*uniqueWords))
#print("Unique words number is {}".format(len(allKey)))
print('C')
def multinomial(l, smoothing):
    line = l.split('\t')
    f_score = math.log(p_future, 10)
    w_score = math.log(p_wise, 10)
    for word in line[1].split(' '):
        if word in allKey.keys():
            if word in future.keys():
                f_score+=math.log((future[word]+smoothing)/(futureWords+smoothing*uniqueWords), 10)
                # print('S1 future, score={}'.format(f_score))
            else:
                if not smoothing == 0:
                    f_score+=math.log((0+smoothing)/(futureWords+smoothing*uniqueWords), 10)
                else:
                    f_score = float('-inf')
            
            if word in wise.keys():
                w_score+=math.log((wise[word]+smoothing)/(wiseWords+smoothing*uniqueWords), 10)
                # print('S1 wise, score={}'.format(w_score))
            else:
                if not smoothing == 0:
                    w_score+=math.log((0+smoothing)/(wiseWords+smoothing*uniqueWords), 10)
                else:
                    w_score = float('-inf')

    return f_score,w_score,(line[0]=='future'and f_score>=w_score or line[0]=='wise'and f_score<=w_score)
        # if line[0] == 'future':
        # elif line[0] == 'wise':

with open(testing) as f:
    content = f.readlines()
    content = [x.strip() for x in content]
print('no smoothing')
line = 0
for c in content:
    line+=1
    f_score, w_score,accuracy = multinomial(c, 0)
    print('{},S{} future_score={}, wise_score={}'.format(accuracy, line, f_score, w_score))

print('add 0.5 smoothing')
line = 0
for c in content:
    line+=1
    f_score, w_score, accuracy = multinomial(c, 0.5)
    print('{},S{} future_score={}, wise_score={}'.format(accuracy, line, f_score, w_score))