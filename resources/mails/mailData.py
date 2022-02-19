
import imp


import pickle


def towho():
    with open('resources/PickleFiles/mailstoend.pkl', 'rb') as f:
        data = pickle.load(f)
    return data




def frowho():
    fro = "academicdons@gmail.com"
    return fro

def puss():
    pas = "Academicdons@254"
    return pas