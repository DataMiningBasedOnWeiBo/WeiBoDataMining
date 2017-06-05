# -*- encoding: utf-8 -*-
from glossary import words
import word
import simword


def get_sim(word1, word2):
    if word1 in words and word2 in words:
        value1 = words[word1]
        value2 = words[word2]
        max_sim = 0
        for item1 in value1:
            attr1 = get_attr(item1)
            for item2 in value2:
                attr2 = get_attr(item2)
                sim = simword.sim_word(attr1, attr2)
                max_sim = max_sim if max_sim > sim else sim
        return max_sim
    else:
        #print('有词没有被收录！')
        return 0


def get_attr(attr):
    word.parse_detail(attr)
    return word.return_attr()
