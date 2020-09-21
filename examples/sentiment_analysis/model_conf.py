from transformers import pipeline

import model_test

model = pipeline("sentiment-analysis")


@model_test.register("invariance")
def invariance_test(example):
    inputs = [e["data"] for e in example]
    output_a, output_b = model(inputs)
    return output_a["label"] == output_b["label"]


@model_test.register("unit")
def unit_test(example):
    output = model(example["data"])[0]
    return output["label"] == example["label"]
