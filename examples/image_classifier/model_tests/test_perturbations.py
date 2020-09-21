import os
import random

import albumentations
import numpy as np
import torchvision.datasets as datasets
from PIL import Image

import model_test
from model_test import USER_CACHE_DIR
from model_test.schemas import Example

dataset = datasets.CIFAR10(USER_CACHE_DIR, train=False, download=True)


@model_test.mark.invariance
def test_inv_rotation(cache_dir, n_examples=5):
    examples = []
    for i in range(n_examples):
        img, label_idx = random.choice(dataset)
        label = dataset.classes[label_idx]
        original_filepath = os.path.join(cache_dir, f"rotate_{label}_{i}.jpg")
        img.save(original_filepath)

        img = np.array(img)
        transform = albumentations.Rotate(limit=5, p=1)
        transformed_img = transform(image=img)["image"]
        transformed_filepath = os.path.join(cache_dir, f"rotate_{label}_{i}_transformed.jpg")
        transformed_img = Image.fromarray(transformed_img)
        transformed_img.save(transformed_filepath)

        examples.append((Example(data=original_filepath), Example(data=transformed_filepath)))
    return examples
