import nlpaug.augmenter.char

import model_test
from model_test.schemas import Example


@model_test.mark.invariance
def test_invariance_keyboard_typo():
    aug = nlpaug.augmenter.char.KeyboardAug()
    examples = []
    sentences = [
        "The weather is so nice out today!",
        "Ugh I can't believe it's not butter",
        "Well... that was surprising",
        "Are you kidding me???",
    ]
    for sentence in sentences:
        typo_sentence = aug.augment(sentence)
        examples.append((Example(data=sentence), Example(data=typo_sentence)))
    return examples
