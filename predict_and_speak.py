import pickle, spacy, read_animations
import en_vectors_glove_md as eng
from read_animations import start, wait
from random import randint
from subprocess import call

nlp = eng.load()
model = pickle.load(open('pickles/perceptron.pickle', 'rb'))

def blank():
    '''
    Prints 1000 blank lines, effectively
    clearing the console.
    '''
    print '\n' * 1000

def process_gesture(category):
    '''
    Processes one of the nine categories
    grouping NAO gestures together.
    
    :param category: Category to explore and generate
                     a behavioral gesture from.
    :return: A random animation fitting the appropriate
             category, ensuring "natural", stochastic output.
    '''
    group = read_animations.grouped_tags[category]
    animations = read_animations.animations_by_tag[group[randint(0, len(group) - 1)]]
    return animations[randint(0, len(animations) - 1)]

def process_input(input):
    '''


    :param input:
    :return:
    '''
    prediction = model.predict(nlp(unicode(input)).vector.reshape(1, -1))
    gesture = process_gesture(prediction[0])  # 0th index is gesture tag.
    return start(gesture) + ' ' + input + ' ' + wait(gesture)

def prompt():
    '''
    

    :return:
    '''
    messages = []
    blank()
    print 'Please input messages for NAO to speak and behave with.'
    print 'Type \'quit\' to exit and save model to disk.\n'
    while True:
        input = raw_input(">>> ")
        if input == 'quit':
            blank()
            break
        messages.append(process_input(input))
    return messages

# Dump the messages to disk & call subprocess for NAO to speak.
pickle.dump(prompt(), open('pickles/messages.pickle', 'wb'))
blank()
print 'Saved messages to disk. Speaking now...\n'

call(['python', 'speech_runner.py'])
