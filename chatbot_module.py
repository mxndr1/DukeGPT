# chatbot_module.py

import random
import json
import pickle
import re
import pyttsx3
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

class Chatbot:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open('intents.json').read())
        self.words = pickle.load(open('words.pkl', 'rb'))
        self.classes = pickle.load(open('classes.pkl', 'rb'))
        self.model = load_model('chatbot_model.h5')

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        Error_Threshold = 0.25
        results = [[i,r] for i, r in enumerate(res) if r > Error_Threshold]

        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
        return return_list

    def text_to_speech(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def solve_math_problem(self, input_string):
        pattern = r'([-+*/\d\s().]+)'

        matches = re.findall(pattern, input_string)

        expression = ''.join(matches)

        try:
            result = eval(expression)
            return result
        except Exception as e:
            return f"Error: {e}"

    def get_response(self,input):
        ints = self.predict_class(input)
        tag = ints[0]['intent']
        list_of_intents = self.intents['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                if tag == "math":
                    result = random.choice(i['responses']) + str(self.solve_math_problem(input))
                else:
                    result = random.choice(i['responses'])
        self.text_to_speech(result)
        return result

