# model_test

`model_test` is a library for testing machine learning models, designed to have a familar user experience for those with experience writing software tests using `pytest`. This library is intended to be a general-purpose model testing framework that supports all of the popular modeling libraries (`scikit-learn`, `pytorch`, `tensorflow`, etc.) 

> Note: this is currently a **proof of concept** exploring what a user experience might look like for a model testing framework.

Model tests are executed in two phases:

1. Define functions to programatically **generate** test cases for your model.
    - For each test case, you will need to specify what *type* (invariance, directional expectation, etc.) of test to run. 
    - This will represent the bulk of your testing code.
    - Return test cases that follow an expected schema.
        - Supported keys: `'data'`, `'label'`, and `'metadata'`
        - For large files (eg. images), save the file and pass a reference to the file in the `data` field. See `examples/image_classifier` for an example.

```
@model_test.mark.invariance
def test_invariance_english_names():
    examples = []
    sentence_pairs = [
        ('I really enjoyed meeting John today', 'I really enjoyed meeting Susie today'),
        ('Do you think Steven was involved?', 'Do you think Mary was involved?'),
    ]
    for sentence_a, sentence_b in sentence_pairs:
        test_case = ({'data': sentence_a}, {'data': sentence_b})
        examples.append(data)
    return examples
```

2. Define code to perform model inference and **evaluate** test cases.
    - Define a function for each test *type* (invariance, directional expectation, etc.) that returns a boolean value denoting whether the model passed that test case.
    - By convention, define these functions in a module named `model_conf.py` in the root of your tests directory.

```
@model_test.register('invariance')
def invariance_test(examples):
    output_a = model(examples[0]['data'])
    output_b = model(examples[1]['data'])
    return output_a["label"] == output_b["label"]
```

There is a simple CLI which makes it easy to execute tests.


## Examples

Check out the `examples/` directory to see how we could write tests for a sentiment classification model and an image classification model.

Setup
```
git clone https://github.com/jeremyjordan/model_test.git
cd model_test
pip install -e .
pip install -r examples/sentiment_analysis/requirements.txt
pip install -r examples/image_classifier/requirements.txt
```

Sentiment classification:
```
model_test generate "examples/sentiment_analysis/"
model_test run "examples/sentiment_analysis/"
```

Image classification:
```
model_test generate "examples/image_classifier/"
model_test run "examples/image_classifier/"
```

# To do

- [ ] Overall design of library, more robust checks
- [ ] Support user defined fixtures
- [ ] Parametrize decorator (with repeat for random sampling)
- [ ] Add domain-specific generator functions to library (eg. `build_inv_pair_from_template`)
- [ ] Highlight data examples that fail tests
- [ ] Save MD5 hash for files referenced in tests
- [ ] Make random seed configurable
- [ ] Brainstorm how to report model coverage
- [ ] Much more...

