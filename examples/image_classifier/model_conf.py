import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

from model_test import register

model = models.resnet50(pretrained=True)
model.eval()

pil_to_tensor = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]
)


def img_to_tensor(img_path: str):
    pil = Image.open(img_path)
    return pil_to_tensor(pil)


@register("invariance")
def invariance_test(examples):
    inputs = torch.stack([img_to_tensor(example["data"]) for example in examples])
    outputs = model(inputs)
    preds = torch.argmax(outputs, axis=1)
    return preds[0].item() == preds[1].item()
