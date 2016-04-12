__author__ = 'Anirudh'

from sys import argv
script,filepath = argv

possibletags = set()
transition = {}
emission = {}

# read the file
file = open(filepath, "r")

line = file.readline()

beginning = "<s>"
while line:
    line = line.strip()
    words = line.split()

    for wordtag in words:
        wtarray = wordtag.split("/")
        words = wtarray[:len(wtarray)-1]
        tag = wtarray[len(wtarray)-1]

        #Append the tag set
        possibletags.add(tag)

        #Update the transition value
        if beginning in transition:
            if tag in transition[beginning]:
                transition[beginning][tag]+=1
            else:
                transition[beginning][tag]=1
            transition[beginning]['count']+=1
        else:
            transition[beginning] = {tag:1,'count':1}


        #update the emission value
        for w in words:
            if w in emission:
                if tag in emission[w]:
                    emission[w][tag]+=1
                else:
                    emission[w][tag] = 1
                emission[w]['count']+=1
            else:
                emission[w]= {tag:1,'count':1}

        beginning = tag

    beginning = "<s>"
    line = file.readline()


#calculate transition probabilities
totaltags = len(possibletags)

for element in transition.iteritems():
    key,value = element
    tagcount = value['count']
    del value['count']

    for tag,count in value.iteritems():
        value[tag]=float(count+1)/float(tagcount+totaltags)

    value['restoftags'] = float(1)/float(tagcount+totaltags)

#calculate emission probabilities
for element in emission.iteritems():
    key,value = element
    wordcount = value['count']
    del value['count']

    for tag,count in value.iteritems():
        value[tag]=float(count)/float(wordcount)


#write file
output = open("hmmmodel.txt","w")

for word,tagdict in emission.iteritems():
    for tag,probability in tagdict.iteritems():
        if len(word) > 0:
            output.writelines(word+" "+tag+" "+str(probability)+"\n")

output.writelines('\n')

for prev,tagdict in transition.iteritems():
    for tag,probability in tagdict.iteritems():
        output.writelines(prev+" "+tag+" "+str(probability)+"\n")
