import nltk
from nltk.corpus import stopwords

import re

"""
since <prd> is used various places apart from the end of conversation, we stored some predecided
prefixes to work specifically around them
"""

prefixes = "(Mr| |Mrs|Ms)[.]"
with open("Text.txt", "r") as f1:
    raw_text = f1.read()
    # here we turn the whole text body into a single line string
    string = " ".join(raw_text.splitlines())
    print(string)


# We've used function below to split the whole sentence into list of seperate sentences.
def split_into_sentences(text):
    text = re.sub(prefixes, "\\1<prd>", text)
    if ".\"" in text:
        text = text.replace(".\"", "<prd>\"")
    text = text.replace(".", ".<stop>")
    text = text.replace("<prd>", ".")
    text = text.replace("n\'", 'n\'')

    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


text_list = split_into_sentences(string)


# First task (without using nltk library)
def find(word):
    word = " " + word + " "
    print(string.count(word))
    [length, quot, status, conversation, sentence] = [0, '"', "No", "", []]

    for i in text_list:
        length += len(i)-2
        # here we tracking the length at which we are so to directly operate in 'string' and get the conversation. 

        if word in i:
            sentence.append(i)

            if i.count(quot) == 1:
                index1 = i.index(quot)
                word_index = i.index(word[0])
                if index1 < word_index:
                    status = "Yes"
                    required_len = length+index1
                    index2 = string.index(quot, required_len+1)
                    conversation_instance = string[required_len:index2]
                    conversation += conversation_instance+","+str(conversation_instance.count(word))+" time"

            elif i.count(quot) == 2:
                index1 = i.index(quot)
                index2 = i.index(quot,index1+1)
                word_index = i.index(word[0])
                if word_index < index2:
                    status = "Yes"
                    conversation = i[index1:index2+1]
                    conversation += conversation+","+str(conversation.count(word))+" time" ","
    if status == "Yes":
        print(f"{sentence}\n{status}, Conversation - {conversation}")
    else:
        print(f"{sentence}\n{status}")


# Second Task
def get_conversation(text):
    n = 0
    index1 = text.index('"')

    while True:
        try:
            index2 = text.index('"', (index1 + 1))
            if n % 2 == 0:
                print(text[index1:index2])
            index1 = index2+1
            n += 1
        except:
            break


# Third task (with the help of nltk library)
def Get_ProperNoun(text):
    print('PROPER NOUNS EXTRACTED :')

    # 1
    sentences = nltk.sent_tokenize(text)

    # 2
    Unrequired_words= stopwords.words('english')
    for sentence in sentences:
        # 3
        words = nltk.word_tokenize(sentence)

        # 4
        words = [word for word in words if word not in Unrequired_words]

        # 5
        tagged = nltk.pos_tag(words)

        # 6
        for (word, tag) in tagged:
            if tag == 'NNP':
                print(word)

"""

Here we used various Pythons NLTK library imports to extract information from the text.

Logic for third task:
    1: we split the paragraph into list of sentences.
    2: then collected all the stopwords as a list from the text given.
    3: Here for every sentence in the list ‘sentences’ we are splitting the sentences into list of words.
    4: we removed the stopwords from the list of words.
    5: here we applied POS tagging to each word in the list.
    6: and at last we filtered the proper noun from list 'words'
    
"""
