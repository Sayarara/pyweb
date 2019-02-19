
import re
from  sigirexperiments import processhelper
from sigirexperiments import  models
from nltk.corpus import wordnet as wn

def patternStringGenerator(seed):

    if seed.isdigit(): # 纯数字
        length = len(seed)
        # print(length)
        strr = r'\b[0-9]{'+str(length)+ r'}\b'
        # print(strr)
        return strr
    else:
        aaa = re.sub("\D", "", seed)
        if len(aaa) > 0: # seed 中包含数字
            restr = [r'\b']
            for i in seed:
                if i.isalpha():
                    restr.append(r'[a-z]')
                else:
                    if i.isdigit():
                        restr.append(r'\d')
                    else:
                        restr.append(r'.')
            restr.append(r'\b')
            restrr = ''.join(restr)
            # print(restr)
            # print(restrr)
            return restrr
        elif seed.isalpha():
            print("is alpha")
            return None
        else:
            if len(seed) > 30:
                # 增加长字串模糊匹配？
                return None
            cleaningseed = processhelper.simpledatacleaning(seed)
            splists = cleaningseed.split(' ')
            if len(splists) > 0:
                restr = [r'\b',splists[0]]
                if len(splists) < 2:
                    a = r'[a-zA-Z]+'
                    restr.append(r'[^a-zA-Z0-9]*')
                    restr.append(a)
                else:
                    for substring in range(1,len(splists)-1):
                        a = r'[a-zA-Z]+'
                        restr.append(r'[^a-zA-Z0-9]*')
                        restr.append(a)
                    restr.append(r'[^a-zA-Z0-9]*')
                    restr.append(splists[len(splists)-1])


                restr.append(r'\b')
                restrr = ''.join(restr)
                print(restrr)
                return restrr






def patternGenerator(seed):

    if seed.isdigit(): # 纯数字
        length = len(seed)
        # print(length)
        strr = r'\b[0-9]{'+str(length)+ r'}\b'
        # print(strr)
        p = re.compile(strr)
        return p
    else:
        if seed.isalpha():
            print("is alpha")
            return None
        else:
            restr =[r'\b']
            for i in seed:
                if i.isalpha():
                    restr.append(r'[a-z]')
                else:
                    if i.isdigit():
                        restr.append(r'\d')
                    else:
                        restr.append(r'.')
            restr.append(r'\b')
            restrr=''.join(restr)
            # print(restr)
            # print(restrr)
            p = re.compile(restrr, re.I)
            return p


def pattersSetGenetorForSeeds(seedslist):
    patternStrs = []
    for seed in seedslist:
        str = patternStringGenerator(seed=seed)
        if str:
            patternStrs.append(str)
    setstr = set(patternStrs)
    ps = []
    for str in setstr:
        ps.append(re.compile(str, re.I))
    return ps


def findCandidateSilbings(seedslist,data):
    ps = pattersSetGenetorForSeeds(seedslist=seedslist)
    matches = []
    for p in ps:
        matches.extend(findmatchs(p=p,data=data))
    return list(set(matches))

def findmatchs(p,data):
    matches = []
    for d in data:
        matches.extend(p.findall(d.text))
    return list(set(matches))

def synonymPatternStrGenerator(pair,value):
    if pair[0] == pair[1]:
        return None
    # check input pattern
    p = patternGenerator(pair[0])
    if p:
        result = p.findall(value)
        if result:
            if set(pair[1]).issubset(set(pair[0])):
                diff = set(pair[0]).difference(set(pair[1]))
                for dif in diff:
                    value = value.replace(dif, '')
                restr = [r'\b', value, r'\b']
                return ''.join(restr)
            # check pair pattern
            lcs, len = processhelper.getNumofCommonSubstr(pair[0], pair[1])
            startpoint = pair[0].find(lcs)
            subvalue = value[startpoint:startpoint + len]
            # simple replace generator
            restr = [r'\b', pair[1].replace(lcs, subvalue), r'\b']
            return ''.join(restr)

def synonymPatternStrGenerator2(pair,value):
    if pair[0] == pair[1]:
        return None
    # check input pattern
    p = patternGenerator(pair[0])
    if p:
        result = p.findall(value)
        if result:
            if set(pair[1]).issubset(set(pair[0])):
                diff = set(pair[0]).difference(set(pair[1]))
                for dif in diff:
                    value = value.replace(dif, '')
                restr = [r'\b', value, r'\b']
                return ''.join(restr)
            # check pair pattern
            lcs, lenn = processhelper.getNumofCommonSubstr(pair[0], pair[1])
            startpoint = pair[0].find(lcs)
            subvalue = value[startpoint:startpoint + lenn]
            subvaluefo = pair[1][startpoint:startpoint + lenn]
            # simple replace generator

            restr = [r'\b']

            if startpoint == 0:
                print(subvalue)
                remaining = pair[1].replace(subvaluefo,'')
                print(remaining)
                restr.append(subvalue)
                length = len(remaining)
                restr.append(r'[a-zA-Z]{' + str(length) + r'}')
            else:
                if startpoint + lenn == len(pair[0]):
                    remaining = pair[1].replace(subvaluefo, '')
                    length = len(remaining)
                    restr.append(r'[a-zA-Z]{' + str(length) + r'}')
                    restr.append(subvalue)
                else:
                    strs = pair[1].split(subvaluefo)
                    length = len(strs[0])
                    restr.append(r'[a-zA-Z]{' + str(length) + r'}')
                    restr.append(subvalue)
                    length = len(strs[1])
                    restr.append(r'[a-zA-Z]{' + str(length) + r'}')
            restr.append(r'\b')

            return ''.join(restr)

def synonymsForCurrentAttr(currentAttr,data):
    Mp = []
    values = models.sigirCoraAttrValue.objects.filter(attr_id=currentAttr.id)
    dict = {}
    for v in values:
        syns = models.sigirCoraValueSynonym.objects.filter(value=v)
        for L in syns:
            if v.value != L.synonym:
                print(tuple([v.value, L.synonym]))
                Mp.append(tuple([v.value, L.synonym]))
    for v in values:
        syns = models.sigirCoraValueSynonym.objects.filter(value=v)
        synslist = [L.synonym for L in syns]
        patternStrs = []
        for p in Mp:
            if p:
                synonymPatternStr = synonymPatternStrGenerator2(p, v.value)
                print(synonymPatternStr)
                if synonymPatternStr not in synslist:
                    patternStrs.append(synonymPatternStr)
        if len(v.value) < 25:
            patternStrs.extend(synsUsingWordNet(v.value))
        setstr = set(patternStrs)
        ps = []
        for str in setstr:
            if str:
                ps.append(re.compile(str, re.I))
        match = []
        for p in ps:
            match.extend(findmatchs(p=p, data=data))
        matches = list(set(match).difference(set(synslist)))
        if len(matches) > 0:
            dict[v.value]=list(set(matches))
    return dict


def synsUsingWordNet(value):
    synsets = wn.synsets(value)
    syns = []
    for syn in synsets:
        syns.extend(syn.lemma_names())
    # print(syns)
    syns = list(set(syns))
    # print(syns)
    wnPatternStr = []
    for syn in syns:
        restr = [r'\b', syn, r'\b']
        temp = ''.join(restr)
        wnPatternStr.append(temp)
    return wnPatternStr

