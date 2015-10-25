import pickle
from nltk.corpus import cmudict
from collections import defaultdict
from syllabizer import *
import random

syllable_dict = pickle.load(open('syllable_dict.pkl', 'rb'))
pronunciations = cmudict.dict()

def stresses(word):
    pronunciation = pronunciations[word]
    stresses = []
    for each in pronunciation:
        temp = tuple(i[-1] for i in each if i[-1].isdigit())
        stresses.append(temp)
    return list(set(stresses))

def stressify(word):
    sylls = syllable_dict[word]
    stress = stresses(word)
    versions = []
    for each in stress:
        for each2 in sylls:
            if len(each) == len(each2):
                versions.append(map(lambda x: x[1].upper() if x[0]==u'1' else x[1], zip(each,each2)))
    if not versions:
        a = Syllabizer()
        return a.Syllabize(word)
    return versions

def converter(sentence):
    stressed = map(stressify, sentence.split())
    maxsylls = sum(map(lambda x: len(max(x, key=len)), stressed))
    minsylls = sum(map(lambda x: len(min(x, key=len)), stressed))
    if maxsylls != minsylls:
        print 'weird...'

    stresschart = range(maxsylls)
    counter = 0
    for each in stressed:
        if len(each) == 2:
            if len(each[0]) == len(each[1]):
                print each
                stresschart[counter] = .5
                counter+=1
        else:
            for syll in each[0]:
                if syll.isupper():
                    stresschart[counter] = 1
                    counter+=1
                else:
                    stresschart[counter] = 0
                    counter+=1
    print stresschart

    return '   '.join(map(lambda x: ' '.join(x), map(random.choice,stressed)))

print converter('i dream of genie')




# syllable_dict = defaultdict(list)
# words = open('Syllables.txt').read().replace('\xb7', ' - ').replace('\r','').replace('\n', ', ').replace('=', ' : ')
# words = words.split(', ')
# words = words[:-1]

# for each in words:
#     each = each.split(' : ')
#     word = each[0]
#     splits = each[1]
#     syllable_dict[word].append(splits.split(' - '))


# pickle.dump(syllable_dict, open('syllable_dict.pkl','wb'))