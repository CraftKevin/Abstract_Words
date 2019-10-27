import sys
from random import random
import os

def str2utf8(s):
    s=s[1:].split('%')
    ret=b''
    for i in s:
        ret+=chr(16*(int(i[0],16))+int(i[1],16)).encode('latin1')
    return ret.decode('utf-8')

def init_data(data_name):
    #load the hanzi list
    global dataDict
    dataList=[]
    with open(data_name,'r') as f:
        dataBuffer=f.read()
    dataListTmp=dataBuffer.replace('\r','').split('\n')
    while True:
        try:
            dataListTmp.remove('')
        except ValueError:
            break
    for i in dataListTmp:
        #i=i.decode('utf-8')
        l=len(i)-1
        while ord('a')<=ord(i[l]) and ord(i[l])<=ord('z'):
            l=l-1
        if l < 0:
            print(i)
            raise Exception('str are all alpha')
        elif l == len(i)-1:
            print(i)
            raise Exception('str has no alpha')
        dataList.append([i[l+1:],i[:l+1]])
    dataDict={}
    for i in dataList:
        if not i[1] in dataDict:
            dataDict[i[1]]=i[0]
        else:
            if len(dataDict[i[1]])<len(i[0]):
                dataDict[i[1]]=i[0]
    #load the emoji list
    global emojiDict
    global emojiList
    with open('EmojiUtf8','r') as f:
        dataBuffer=f.read()
    emojiList=[[str2utf8(i.split(',')[0]),i.split(',')[1]] for i in dataBuffer.split('\n')]
    emojiDict={i[1]:i[0] for i in emojiList}
    
    #loadd the absinfo
    global absDict
    with open('emoji/emoji.txt','r') as f:
        absBuffer=f.read()
    absBuffer=[i.split(',') for i in absBuffer.split('\n')]
    absDict={}
    for i in absBuffer:
        for j in i[1:]:
            if j=='-':
                continue
            if j in absDict:
                absDict[j].append(i[0])
            else:
                absDict[j]=[i[0]]
                
import cv2
def deal_emoj():
    global emojiList
    if not os.path.exists('emoji'):
        raise Exception('no emoji in dir')
    if not os.path.exists('emoji/emoji.txt'):
        tmp=[i[1] for i in emojiList]
        with open('emoji/emoji.txt','w+') as f:
            f.write('\n'.join(tmp))
    with open('emoji/emoji.txt','r') as f:
        emojiBuffer=f.read().replace(' ','')
    dealList=[i.split(',') for i in emojiBuffer.split('\n')]
    i=0
    #0 is in order
    mode=0
    while True:
        if mode==0:
            while i < len(dealList) and (not len(dealList[i])==1):
                i+=1
            if i==len(dealList):
                print('done with 0 mode')
                break
            cv2.imshow('test',cv2.imread('emoji/'+dealList[i][0]))
            cv2.waitKey(100)
            print('input the %s'%dealList[i][0])
            inp=input().replace(' ','').replace('\n','').replace('\t','').lower()
            if inp=='':
                break
            if not inp in dealList[i]:
                dealList[i].append(inp)
            i+=1
        else:
            raise Exception('known mode')
    with open('emoji/emoji.txt','w+') as f:
        f.write('\n'.join([','.join(i) for i in dealList]))

def is_space(s):
    if s==' ' or s=='\t' or s=='\r' or s=='\f' or s=='\n':
        return True
    else:
        return False
def is_alpha(s):
    if (s>='a' and s<='z') or (s>='A' and s<='Z'):
        return True
    else:
        return False
    
def str2abs(s):
    global dataDict
    global emojiDict
    global absDict
    #split s to word
    wordList=[]
    i=0
    while True:
        if i == len(s):
            break
        print(s[i])
        if ord(s[i])>255:
            #not ascii
            if s[i] in dataDict:
                tmp=[]
                tmp.append(s[i])
                tmp.append(dataDict[s[i]])
                wordList.append(tmp)
            else:
                #other language
                wordList.append(s[i])
            
        elif is_alpha(s[i]):
            #english word
            j=i
            while j<len(s) and is_alpha(s[j]):
                j+=1
            wordList.append(s[i:j])
            i=j-1
        else:
            wordList.append(s[i])
        i+=1
    i=0
    absList=[]
    print('wordList: ')
    print(wordList)
    while True:
        if i==len(wordList):
            break
        if type(wordList[i])==list:
            #chiness
            conNum=1
            j=i+1
            conPyList=[wordList[i][1]]
            while j<len(wordList) and type(wordList[j])==list:
                conPyList.append(wordList[j][1])
                j+=1
                conNum+=1
            print('conPyList:')
            print(conPyList)
            while True:
                if conNum<=0:
                    break
                tmp=''.join(conPyList[:conNum])
                if tmp in absDict:
                    break
                else:
                    conNum-=1
            if not conNum == 0:
                absList.append(absDict[tmp])
                i+=conNum-1
            else:
                absList.append(wordList[i][0])
        else:
            #else
            if wordList[i] in absDict:
                absList.append(absDict[wordList[i]])
            else:
                absList.append(wordList[i])
        i+=1
    #get the final result with a random way
    ret=''
    for i in absList:
        if type(i)==list:
            ret+=emojiDict[i[int(random()*10000)%len(i)]]
        else:
            ret+=i
    return ret

def main():
    global dataDict
    global emojiDict
    global emojiDict
    #deal_emoj()
    print(str2abs('你是真滴牛皮'))
    with open('test.html','w+') as f:
        f.write(''.join(emojiDict.values()))
    
if __name__ == '__main__':
    init_data('Asa_PinYin')
    main()
