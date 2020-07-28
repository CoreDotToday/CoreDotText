# -*- coding: utf-8 -*-

import MeCab
import sys
import string

# Deprecated : PYTHON3
# def testunicode(d):
#     if type(d) == unicode:
#         return d.encode('utf-8')
#     else:
#         return d
# def testunicode2(d):
#     if type(d) != unicode:
#         return d.decode('utf-8')
#     else:
#         return d


def all(sent):
    # sent = testunicode(sent)
    t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic/')
    t.parse('')
    m = t.parse(sent)
    return m


def mordict(sent):
    # sent = testunicode(sent)
    t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic/')
    t.parse('')
    m = t.parseToNode(sent)
    count = 0
    result = dict()
    while m:
        feature = m.feature.split(',')[0]
        if feature != 'BOS/EOS':
            result[count] = [feature, m.surface]
        m = m.next
        count += 1
    return result


def morpheme(sent, mor=['NNG','NNP'], p=0):
    try:
        if type(sent) == list:
            temp = []
            for i in sent:
                t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic/')
                t.parse('')
                m = t.parseToNode(i)
                parsed = []
                while m:
                    if type(mor) == list:
                        if m.feature.split(',')[0] in mor:
                            parsed.append(m.surface)
                    else:
                        if m.feature.split(',')[0]==mor:
                            parsed.append(m.surface)
                    m = m.next
                temp.append(parsed)
            if p!=0:
                for j in temp:
                    print('[%s]' % ', '.join(map(str, j)))
            return temp

        else:
            t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic/')
            t.parse('')
            m = t.parseToNode(sent)
            parsed = []
            while m:
                if type(mor) == list:
                    if m.feature.split(',')[0] in mor:
                        parsed.append(m.surface)
                else:
                    if m.feature.split(',')[0]==mor:
                        parsed.append(m.surface)
                m = m.next
            if p!=0:
                print('[%s]' % ', '.join(map(str, parsed)))
            return parsed

    except RuntimeError:
        print("RuntimeError:", RuntimeError)


def subject(sent):
    if sent == None:
        return []
    # sent = testunicode(sent)
    t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic/')
    t.parse('')
    m = t.parseToNode(sent)
    temp = []
    while m:
        if m.feature.split(',')[0] in ['JKS','JX','JC','JKB','JKG','JKO','VCP','VCP+ETM','XSV+ETM','XSV+EP','XSV']:
            comp = ''
            i=1
            n=m
            while i:
                if n.prev.feature.split(',')[0] in ['SC','SN','NNBC','NNG','NNP','NR','NP'] and n.prev.prev.feature.split(',')[0] not in ['MM']:
                    """
                    선언	NN,T,선언,*,*,*,*,*
                    했	XSV+EP,T,했,Inflect,XSV,EP,하/XSV+ㅕㅆ/EP,*
                    다	EF,F,다,*,*,*,*,*
                    """
                    if comp == '':
                        comp = n.prev.surface
                    else:
                        if n.prev.feature.split(',')[0] in ['NR','SN']:
                            comp = n.prev.surface+comp
                        else:
                            comp = n.prev.surface+' '+comp
                    n = n.prev
                else:
                    i=0
                    # look at the function core
                    #if comp[:6] == '이날':
                    #    comp = comp[7:]
                    #if comp[:6] == '이번':
                    #    comp = comp[7:]
                    if comp != '':
                        temp.append(comp)
        m = m.next
    if temp == []:
        return []
    else:
        #print '[%s]' % ','.join(map(str, temp))
        return temp


def prior(sent, morpheme):
    if type(morpheme) != list:
        morpheme = [morpheme]
    # sent = testunicode(sent)
    t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic/')
    t.parse('')
    m = t.parseToNode(sent)
    temp = []
    while m:
        if m.feature.split(',')[0] in morpheme:
            comp = ''
            i=1
            n=m
            while i:
                if n.prev.feature.split(',')[0] in ['SL','SN','NNP','NNG','NR','NP'] and n.prev.prev.feature.split(',')[0] not in ['MM']:
                    """
                    선언	NN,T,선언,*,*,*,*,*
                    했	XSV+EP,T,했,Inflect,XSV,EP,하/XSV+ㅕㅆ/EP,*
                    다	EF,F,다,*,*,*,*,*
                    """
                    if comp == '':
                        comp = n.prev.surface
                    else:
                        if n.prev.feature.split(',')[0] == 'NR':
                            comp = n.prev.surface+comp
                        else:
                            comp = n.prev.surface+' '+comp
                    n = n.prev
                else:
                    i=0
                    if comp != '':
                        if m.surface == '와':
                            continue
                        temp.append(comp)
        m = m.next
    if temp == []:
        None
        #return []
    else:
        #print '[%s]' % ','.join(map(str, temp))
        return temp


def when(sent):
    # sent = testunicode(sent)
    t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic/')
    t.parse('')
    m = t.parseToNode(sent)
    temp = []
    while m:
        if m.feature.split(',')[0] in ['NNB']:
            nnb = m.surface
            comp = ''
            i=1
            n=m
            while i:
		#if n.prev.feature.split(',')[0] in ['NNB'] and n.prev.prev.feature.split(',')[0] not in ['MM']:
                if n.prev.feature.split(',')[0] in ['SN', 'SY', 'NNB']:
                    """
                    선언	NN,T,선언,*,*,*,*,*
                    했	XSV+EP,T,했,Inflect,XSV,EP,하/XSV+ㅕㅆ/EP,*
                    다	EF,F,다,*,*,*,*,*
                    """
                    if comp == '':
                        comp = n.prev.surface
                    else:
                        if n.prev.feature.split(',')[0] == 'NR':
                            comp = n.prev.surface+comp
                        else:
                            comp = n.prev.surface+' '+comp
                    n = n.prev
                else:
                    i=0
                    if comp != '':
                        temp.append(comp+nnb)
        m = m.next
    if temp == []:
        None
        #return []
    else:
        #print '[%s]' % ','.join(map(str, temp))
        return temp


def who(sent):
    # sent = testunicode(sent)
    t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic/')
    t.parse('')
    m = t.parseToNode(sent)
    temp = []
    who1 = []
    who2 = []
    when = []
    where = []
    what = []
    how = []

    while m:
        feature = m.feature.split(',')
        #if feature[0] in ['NNP'] and feature[1] == '인명':

        # WHO
        if feature[1] in ['인명']:
            # print 'Who1', m.surface
            who1.append(m.surface)
        elif feature[0] in ['JKS','JX'] and m.prev.surface != '명':
            comp = ''
            i=1
            n=m
            while i:
                #if n.prev.feature.split(',')[0] in ['NNG','NNP','Sl','SSO','SN','SY','SSC','NR']:
                if n.prev.feature.split(',')[0] in ['NNG','NNP','Sl','SN','NR']:
                    if comp == '':
                        comp = n.prev.surface
                    else:
                        comp = n.prev.surface+' '+comp
                    n = n.prev
                else:
                    i=0
                    if comp:
                        # print 'Who2', comp
                        who2.append(comp)
        # WHERE
        elif feature[1] in ['지명']:
            # print 'Where', m.surface
            where.append(m.surface)
            #temp.append(comp+nnb)

        # WHAT
        elif feature[0] in ['JKO', 'JKB'] and m.prev.surface != '명':
            comp = ''
            i=1
            n=m
            while i:
                if n.prev.feature.split(',')[0] in ['NNG','NNP','NNB','NNBC','SL','SSO','SN','SY','SSC','NR']:
                    if comp == '':
                        comp = n.prev.surface
                    else:
                        comp = n.prev.surface+' '+comp
                    n = n.prev
                else:
                    i=0
                    if comp:
                        # print 'What', comp
                        what.append(comp)
        # HOW
        elif feature[0] in ['VV+EP','XSV+EP','EP']:
            comp = ''
            n=m
            if 1:
                if n.next.feature.split(',')[0] in ['EF']:
                    prev = n.prev.feature.split(',')[0]
                    if n.prev.prev == None:
                        m = m.next
                        continue
                    pprev = n.prev.prev.feature.split(',')[0]

                    if prev in ['VV','NNG'] and pprev not in ['MM']:
                        comp = n.prev.surface+n.surface+n.next.surface
                    else:
                        comp = n.surface+n.next.surface
                    # print 'How', comp
                    how.append(comp)
                elif n.next.feature.split(',')[0] in ['EC']:
                    prev = n.prev.feature.split(',')[0]
                    if n.prev.prev == None:
                        m = m.next
                        continue
                    pprev = n.prev.prev.feature.split(',')[0]
                    nex = n.next.surface.replace('고','').replace('으며','다')
                    if prev in ['XSV','VV','NNG'] and pprev not in ['MM']:
                        comp = n.prev.surface+n.surface+nex
                    else:
                        comp = n.surface+nex
                    #comp = n.prev.surface+n.surface+n.next.surface.replace('고','')
                    how.append(comp)
        # WHEN
        elif feature[0] in ['NNBC']:
            comp = ''
            n=m
            if 1:
                if n.prev.feature.split(',')[0] in ['SN'] and '명' != n.surface:
                    comp = n.prev.surface+n.surface
                    # print 'When', comp
                    when.append(comp)


        m = m.next

    return [who1, who2, when, where, what, how]
    """
    if temp == []:
        None
        #return []
    else:
        #print '[%s]' % ','.join(map(str, temp))
        return temp
    """


def elements(sent):
    try:
        # sent = testunicode(sent)
        t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic/')
        t.parse('')
        m = t.parseToNode(sent)
        parsed = []
        while m:
            if m.surface != '':
                parsed.append([str(m.surface), m.feature.split(',')[0]])
            m = m.next
        return parsed

    except RuntimeError:
        print("RuntimeError:", RuntimeError)


def core(text):
    result = []
    subjlist = subject(text)
    passlist = ['이날', '올해', '처음', '이번', '다음'] # daumsoft
    removelist = ['이날', '당초', '지난해', '때', '뒤', '급', '만일', '오전', '오후', '이번', '후', '최근', '한편', '이번', '지난달', '오늘', '당일', '그동안', '요즘', '오전', '오후', '가운데', '현재', '경우']
    for word in subjlist:
        if word not in passlist:
            split = word.split(' ')
            if len(split)>1:
                for j in removelist:
                    if j in split[0]:
                        word = word.replace(j+' ', '')
            split = word.split(' ')
            if len(split)>1:
                for j in removelist:
                    if j in split[0]:
                        word = word.replace(j+' ', '')
            #if len(word)>5:
            if len(word)>2:
                # len('12일') is 5
                #word = word.replace(', ', '')
                #result.append(word)

                # Detect the comma between numbers
                # 98년 1월말 123억6,000만달러, 3월말 241억5,000만달러, 5월말 343억5,000만달러, 7월말 392억6,000만달러, 9월말 433억7,000만달러, 11월말 464억7,000만달러로 꾸준히 증가했다.
                # 면허시험이 개선되면 종전에 치르던 신경과, 피부과, 안과, 이비인후과,   비뇨기과, 방사선과, 마취과, 임상병리과 등 8개 과목은 시험과목에서 제   외되며 이들 진료과목은 의사면허 취득후 전공의 과정에서 심도있게 전문   의 수련을 받게 된다.
                commapos = findcomma(word)
                number = [str(j) for j in range(10)]
                start = 0
                for i in commapos:
                    if i-1>0 and i+2 <= len(word):
                        if word[i-1] in number and (word[i+1] in number or word[i+2] in number):
                            continue
                        else:
                            tempword = word[start:i].replace(', ', ',')
                            if tempword[0] in [' ', ',']:
                                tempword = tempword[1:]
                            result.append(tempword)
                            start = i+1
                # for final word
                # , 이비인후과 , 비뇨기과 , 방사선
                if len(commapos)>0 and i<len(word):
                    result.append(word[i:])
                # if word have no comma
                elif start == 0:
                    if word[0] == ' ':
                        word = word[1:]
                    result.append(word)

    # remove functual marks
    fresult = []
    for r in result:
        if len(r)<1:
            continue
        f = r
        if r[0] in [' ', ',']:
            f = r[1:]
        if len(r)>1:
            if r[0:2] in [', ']:
                f = r[2:]
        fresult.append(f)

    return fresult


def findcomma(s):
    pos = []
    for idx, i in enumerate(s):
        if i == ',':
            pos.append(idx)
    return pos
