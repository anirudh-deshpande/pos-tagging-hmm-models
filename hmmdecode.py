__author__ = 'Anirudh'

import sys

from sys import argv
script,filepath = argv

transition = {}
possibletags = set()
emission = {}


# Read the model
model_file = open('hmmmodel.txt','r')

line = model_file.readline()
line = line.strip('\n')
line = line.rstrip(' ')

while len(line) > 1:

    line = line.strip('\n')
    line = line.lstrip(' ')

    elements = line.split(" ")

    if elements[0] in emission:
        emission[elements[0]][elements[1]] = float(elements[2])
    else:

        try:
            elements[2]
        except IndexError:
            print repr(elements[0])
            print elements[0]
            print "Exception"
            continue

        emission[elements[0]]={elements[1]:float(elements[2])}

    line = model_file.readline()

line = model_file.readline()

while line:

    line = line.strip('\n')
    line = line.rstrip(' ')

    elements = line.split(" ")

    possibletags.add(elements[0])

    if elements[0] in transition:
        transition[elements[0]][elements[1]] = float(elements[2])
    else:

        try:
            elements[2]
        except IndexError:
            print repr(elements[0])
            print elements[0]
            print "Exception"
            continue

        transition[elements[0]]={elements[1]:float(elements[2])}

    line = model_file.readline()


# Read the file

file = open(filepath,"r")
outputfile = open('hmmoutput.txt',"w")

line = file.readline()

while line:

    line = line.strip()

    best_edge = [] # For source
    best_score = {'<s>':1.0} # For Probability

    words = line.split()

    for word in words:

        wtlist = {}
        flap = False

        if word not in emission:
            for key in best_score:
                for tag in transition[key]:
                    if tag != 'restoftags':
                        wtlist[tag] = 1.0
            flap = True

        else:
            wtlist = emission[word]
            wtags = set(wtlist.keys())

            for key in best_score:
                tags = set(transition[key].keys())
                if set(tags).intersection(wtags):
                    flap = True
                    break

        edgelist = {}
        probability_word = {}

        for prev,prevprobabolity in best_score.iteritems():
            for tag,emissionprobability in wtlist.iteritems():
                transitionprobability = 0.0

                if flap:
                    if tag in transition[prev]:
                        transitionprobability = transition[prev][tag]
                    else:
                        transitionprobability = transition[prev]['restoftags']

                state_probability = prevprobabolity * emissionprobability * transitionprobability

                if tag not in probability_word or state_probability>probability_word[tag]:
                    edgelist[tag]=prev
                    probability_word[tag] = state_probability


        best_score = probability_word
        best_edge.append(edgelist)

        # print best_score

    taglist = []
    maxval = -1*2147483647
    tag_best = None

    for key,value in best_score.iteritems():
        if value > maxval:
            tag_best = key
            maxval = value

    tag_prev = tag_best
    taglist.append(tag_best)


    for index in xrange(len(best_edge)-1,0,-1):
        tag = best_edge[index][tag_prev]
        tag_prev=tag
        taglist.append(tag)

    out_words = []
    taglist.reverse()

    for index,word in enumerate(words):
        out_words.append('%s/%s' % (word,taglist[index]))

    out_lines = ' '.join(out_words)

    outputfile.write('%s\n' % out_lines)

    line = file.readline()

outputfile.close()