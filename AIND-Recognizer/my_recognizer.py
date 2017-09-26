import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    for i in range(len(test_set.get_all_Xlengths())):
        current_X, current_length = test_set.get_item_Xlengths(i)
        probs_i = {}
        highest_score_word = None
        highest_score = float('-inf')
        for model_key in models.keys():
            try:
                logL = models[model_key].score(current_X, current_length)
                probs_i[model_key] = logL
                if logL > highest_score:
                    highest_score = logL
                    highest_score_word = model_key
            except:
                probs_i[model_key] = float('-inf')
        probabilities.append(probs_i)
        guesses.append(highest_score_word)
    return probabilities, guesses
