import os


ABS_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_DIR_PATH = os.path.join(ABS_PATH, '..', '..', 'data')

SUPERTAGS_PATH = os.path.join(DATA_DIR_PATH, 'supertags.txt')

DANE_POZYTYWISTYCZNE_DIR_PATH = os.path.join(DATA_DIR_PATH,
                                             'dane_pozytywistyczne')

BIGRAMS_PATH = os.path.join(DATA_DIR_PATH, 'poleval_2grams.txt')

POLEVAL_SENTENCES_PATH = os.path.join(DATA_DIR_PATH, 'task3_train.txt')
