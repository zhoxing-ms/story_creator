import datetime
import random
import os
import torch

from diffusers import StableDiffusionPipeline
import openvino.torch # this import is required to activate the openvino backend for torchdynamo

model_id = "stabilityai/stable-diffusion-2-1-base"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)

pipe.unet = torch.compile(
    pipe.unet,
    backend="openvino",
    options={"device": "CPU", "model_caching": "True"},
)

def generate_image_from_text(image_desc):
    random_image_name = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join([str(random.randint(1,10)) for i in range(5)])
    image_path = os.path.join("temp", "image", random_image_name + ".jpg")
    image = pipe(image_desc).images[0]
    image.save(image_path)
    return image_path

if __name__ == '__main__':
    generate_image_from_text("a photo of an astronaut riding a horse on mars")