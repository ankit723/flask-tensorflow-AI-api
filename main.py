import random
import json
import pickle

import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model
lematizer = WordNetLemmatizer()
intents = json.loads(open('data/intents.json').read())

words = pickle.load(open('data/words.pkl', 'rb'))
classes = pickle.load(open('data/classes.pkl', 'rb'))
model = load_model('data/kelvinmodel.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lematizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i]=1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r>ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse = True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability':str(r[1])})
    
    return return_list

def respond(query, intent_json=intents):
    try:
        intent_list = predict_class(query)
        tag = intent_list[0]['intent']
        list_of_intents = intent_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                if "is_setting" in i.keys():
                    is_setting = i["is_setting"]
                else:
                    is_setting = False

                if "setting_value" in i.keys():
                    setting_value = i["setting_value"]
                else:
                    setting_value = None
                break
        json_api =  {
                        "Tag": tag,
                        "Result": result,
                        "is_settings": is_setting,
                        "setting_value": setting_value
                    }
        return json_api
    except IndexError:
        res_main()

def res_main(data):
    return(respond(data))

if __name__ == "__main__":
    res_main('hey')