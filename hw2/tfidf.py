import re
from collections import Counter
import math

def clean(f):
    file = open(f)
    cleanWords = [];
    for line in open(f):
        for word in line.split():
            if(re.match('((http://)|https://)', word)):
                continue
            word = re.sub('[\W]+', '', word)
            cleanWords.append(word.lower())
    file.close()
    return cleanWords

def removeStopwords(words):
    f = open('stopwords.txt', 'r')
    stopwords = f.read().split()
    retWords = []
    for word in words:
        if (word in stopwords):
            continue
        else:
            retWords.append(word)
    f.close()
    return retWords  

def reduceWords(words):
    ret = []
    for word in words:
        word = re.sub('(ing|ly|ment)$', '', word)
        ret.append(word)
    return ret

def printWordsToFile(words, filename):
    fileToMake = 'preproc_' + filename
    f = open(fileToMake, 'w')
    i = 0
    length = len(words) - 1
    for word in words:
        f.write(word + ' ') if i != length else f.write(word)
        i += 1

def preprocess():
    fileNames = []
    for line in open('tfidf_docs.txt'):
        fileName = line.strip()
        fileNames.append('preproc_' + fileName)
        cleanWords = clean(fileName)
        stopwordsRemoved = removeStopwords(cleanWords)
        reducedWords = reduceWords(stopwordsRemoved)
        printWordsToFile(reducedWords, fileName)
    return fileNames

def computeTF(words, allWordsCtr):
    ret = []
    wordCounts = Counter(words)
    allWordsCtr.update(wordCounts.keys())
    numWords = sum(wordCounts.values())
    for item in wordCounts.items():
        TFscore = item[1]/numWords
        ret.append((item[0], TFscore))
    return ret

def computeIDF(ctr, numDocs):
    IDFDict = {}
    ctrList = list(ctr.items())
    for t in ctrList:
        word = t[0]
        count = t[1]
        IDFDict[word] = math.log((numDocs/count)) + 1
    return IDFDict  

def computeTFIDF(TFs, IDF):
    TFIDFs = []
    for TF in TFs:
        TFIDF = []
        for i in TF:
            word = i[0]
            scoreTF = i[1]
            scoreIDF = IDF[word]
            scoreTFIDF = round(i[1] * IDF[word], 2)
            TFIDF.append((word, scoreTFIDF))
        TFIDFs.append(TFIDF)
    return TFIDFs

def printTopFiveScores(scoresList, files):
    i = 0
    for file in files:
        fw = 'tfidf' + file[7:]
        f = open(fw, 'w')
        sortedScores = sorted(scoresList[i], key = lambda t: (-t[1], t[0]))
        f.write(str(sortedScores[:5]))
        i += 1

def computeScores(files):
    numDocs = len(files)
    TFs = []
    allWordsCtr = Counter()
    for f in files:
        words = []
        for line in open(f):
            line = line.strip()
            words.extend(line.split())
        TFs.append(computeTF(words, allWordsCtr))
    IDF = computeIDF(allWordsCtr, numDocs)
    TFIDFs = computeTFIDF(TFs, IDF)
    printTopFiveScores(TFIDFs, files)

def textProcessing():
    files = preprocess()
    computeScores(files)

def main():
    textProcessing()

main()