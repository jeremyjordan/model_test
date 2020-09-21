import random
from string import Formatter

import model_test
from model_test.schemas import Example

formatter = Formatter()

NAMES = ["John", "Cindy", "Trey", "Jordan", "Sam", "Taylor", "Charlie", "Veronica"]
COMPANIES = ["Target", "Amazon", "Google", "Lowes", "Macys"]
POS_ADJS = ["phenomenal", "great", "terrific", "helpful", "joyful"]
NEG_ADJS = ["terrible", "boring", "awful", "lame", "unhelpful", "lackluster"]
NOUNS = ["doctor", "nurse", "teacher", "server", "guide"]
LEXICON = {
    "name": NAMES,
    "company": COMPANIES,
    "pos_adj": POS_ADJS,
    "neg_adj": NEG_ADJS,
    "noun": NOUNS,
}


def build_inv_pair_from_template(template: str, inv_field: str):
    """
    Create a pair of two strings which substitue words from a lexicon into
    the provided template. All fields will have the same value substituted
    in both strings except for the provided invariance field.
    """
    _, fields, _, _ = zip(*formatter.parse(template))
    base_values = {field: random.choice(LEXICON[field]) for field in fields}
    base_values[inv_field] = f"{{{inv_field}}}"
    base_string = formatter.format(template, **base_values)
    inv_field_selections = random.sample(LEXICON[inv_field], k=2)
    inv_field_values = [{inv_field: value} for value in inv_field_selections]
    string_a = formatter.format(base_string, **inv_field_values[0])
    string_b = formatter.format(base_string, **inv_field_values[1])
    return string_a, string_b


@model_test.mark.invariance
def test_name_invariance_positive_statements():
    templates = [
        ("{name} was a {pos_adj} {noun}", 15),
        ("I had {name} as a {noun} and it was {pos_adj}", 20),
        ("{name} is {pos_adj}", 3),
    ]
    examples = []
    for template, n_examples in templates:
        for _ in range(n_examples):
            input_a, input_b = build_inv_pair_from_template(template, "name")
            examples.append((Example(data=input_a), Example(data=input_b)))
    return examples


@model_test.mark.invariance
def test_name_invariance_negative_statements():
    templates = [
        ("I had an {neg_adj} experience with {name}", 15),
        ("{name} is a {neg_adj} {noun}", 15),
        ("are you kidding me? {name} is {neg_adj}", 5),
    ]
    examples = []
    for template, n_examples in templates:
        for _ in range(n_examples):
            input_a, input_b = build_inv_pair_from_template(template, "name")
            examples.append((Example(data=input_a), Example(data=input_b)))
    return examples


@model_test.mark.unit
def test_short_positive_phrases():
    examples = []
    sentences = ["I like you", "You look happy", "Great!", "ok :)"]
    for sentence in sentences:
        examples.append(Example(data=sentence, label="POSITIVE"))
    return examples
