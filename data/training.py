import random
import json
import pickle
from matplotlib.font_manager import json_load
import numpy as np

import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

import tensorflow as tf
sequential = tf.keras.models.Sequential
dense = tf.keras.layers.Dense
dropout = tf.keras.layers.Dropout
activation = tf.keras.layers.Activation
sgd = tf.keras.optimizers.SGD

lematizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ingnore_letters = ['?', '!', ',', '.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words=[lematizer.lemmatize(word) for word in words if word not in ingnore_letters]
words = sorted(set(words))

classes=sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))


training = []
output_empty = [0]*len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns=[lematizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row=list(output_empty)
    output_row[classes.index(document[1])]=1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)
train_x = list(training[:,0])
train_y = list(training[:,1])

model = sequential()
model.add(dense(128, input_shape = (len(train_x[0]),), activation='relu'))

model.add(dropout(0.5))
model.add(dense(64, activation='relu'))
model.add(dropout(0.5))
model.add(dense(len(train_y[0]), activation='softmax'))

Sgd = sgd(lr = 0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=Sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size = 5, verbose = 1)
model.save('kelvinmodel.h5', hist)
print('done')



