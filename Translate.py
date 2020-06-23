#Translates the romanji to hiragana


import Error


hiragana = {'a':"あ", 'i':"い", 'u':'う', 'e':'え', 'o':'お', 'ka':"か", 'ki':"き", 'ku':'く', 'ke':'け', 'ko':'こ', 'sa':"さ", 'shi':"し", 'su':'す', 'se':'せ', 'so':'そ', 'ta':"た", 'chi':"ち", 'tsu':'つ', 'te':'て', 'to':'と',
            'na':"な", 'ni':"に", 'nu':'ぬ', 'ne':'ね', 'no':'の', 'ha':"は", 'hi':"ひ", 'fu':'ふ', 'he':'へ', 'ho':'ほ', 'ma':"ま", 'mi':"み", 'mu':'む', 'me':'め', 'mo':'も', 'ra':"ら", 'ri':"り", 'ru':'る', 're':'れ', 'ro':'ろ',
            'ya':"や", 'yu':'ゆ', 'yo':'よ', 'wa':"わ", 'wo':'を', 'n':'ん', 'ga':"が", 'gi':"ぎ", 'gu':'ぐ', 'ge':'げ', 'go':'ご', 'za':"ざ", 'ji':"じ", 'zu':'ず', 'ze':'ぜ', 'zo':'ぞ', 'da':"だ", 'di':"ぢ", 'du':'づ', 'de':'で', 'do':'ど'
            , 'ba':"ば", 'bi':"び", 'bu':'ぶ', 'be':'べ', 'bo':'ぼ', 'pa':"ぱ", 'pi':"ぴ", 'pu':'ぷ', 'pe':'ぺ', 'po':'ぽ', 'xtsu':'っ', 'sho':'しょ', 'sha':'しゃ', 'shu':'しゅ', 'kya':'きゃ', 'kyo':'きょ', 'kyu':'きゅ',  'jo':'じょ',
            'ja':'じゃ', 'ju':'じゅ', 'gya':'きゃ', 'gyo':'きょ', 'gyu':'ぎゅ'}



def TranslateHiragana(string):
    sentence = ''
    stringList = string.split()
    for word in stringList:
        sentence += Hiragana(word)
        if(word != stringList[len(stringList) - 1]):
            sentence += ' '
    return sentence


def Hiragana(word):
    newWord = ''
    count = 0
    while count < len(word):
        newSyllable = ''

        if (word[count].lower() == 'k'):
            if (word[count + 1].lower() == 'y'):
                newSyllable += "ky"
                newSyllable = AddVowel(word[count + 2], newSyllable)
            else:
                newSyllable += "k"
                newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 'g'):
            newSyllable += "g"
            newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 's'):
            if (word[count + 1].lower() == 'h'):
                newSyllable += "sh"
                newSyllable = AddVowel(word[count + 2], newSyllable)
            else:
                newSyllable += "s"
                newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 'z'):
                newSyllable += "z"
                newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 'j'):
            newSyllable += "j"
            newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 't'):
            if (word[count + 1].lower() == 's'):
                newSyllable += "ts"
                newSyllable = AddVowel(word[count + 2], newSyllable)
            else:
                newSyllable += "t"
                newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 'd'):
            newSyllable += "d"
            newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 'c'):
            if (word[count + 1].lower() == 'h' and word[count + 2].lower() == 'i'):
                newSyllable = 'chi'
            else:
                raise Error.UnknownWordError(word, 'The Hiragana for this romanji could not be found', newSyllable)

        elif (word[count].lower() == 'n'):
            if (count == len(word) - 1):
                newSyllable += 'n'
            else:
                newSyllable += "n"
                newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 'h'):
            newSyllable += "h"
            newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 'b'):
            newSyllable += "b"
            newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 'p'):
            newSyllable += "p"
            newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 'm'):
            newSyllable += "m"
            newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 'r'):
            newSyllable += "r"
            newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 'w'):
            newSyllable += "w"
            newSyllable = AddVowel(word[count + 1], newSyllable)

        elif (word[count].lower() == 'y'):
            newSyllable += "y"
            newSyllable = AddVowel(word[count + 1], newSyllable)

        else:
            newSyllable = AddVowel(word[count])

        if(newSyllable == 'Unknown'):
            raise Error.UnknownWordError(word, 'The Hiragana for this romanji could not be found', newSyllable)

        elif (newSyllable[0] == 'x'):
            count += len(newSyllable) - 3

        else:
            count += len(newSyllable)

        if newSyllable in hiragana.keys():
            newWord += hiragana.get(newSyllable)

    return newWord

def AddVowel(vowel, letter = None):
    if (vowel.lower() == 'a' or vowel.lower() == 'i' or vowel.lower() == 'u' or vowel.lower() == 'e' or vowel.lower() == 'o'):
        if (letter != None):
            syllable = letter + vowel
        else:
            syllable = vowel
        return syllable

    elif(letter != None):
        if (vowel.lower() == letter.lower() and vowel.lower() != 'n'):
            syllable = 'xtsu'
            return syllable
        elif (letter.lower() == 'n'):
            syllable = 'n'
            return syllable
    return "Unknown"
