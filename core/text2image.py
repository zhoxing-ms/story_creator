import datetime
import random
import os

from optimum.intel import OVLatentConsistencyModelPipeline
from pathlib import Path

ov_pipeline = OVLatentConsistencyModelPipeline.from_pretrained("model/lcm", export=False, compile=False)
ov_pipeline.reshape(batch_size=1, height=512, width=512, num_images_per_prompt=1)
ov_pipeline.to("GPU")
ov_pipeline.compile()

def generate_image_from_text(image_desc):
    random_image_name = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join([str(random.randint(1,10)) for i in range(5)])
    image_path = os.path.join("temp", "image", random_image_name + ".jpg")
    image_ov = ov_pipeline(prompt=image_desc, num_inference_steps=4, guidance_scale=8.0, height=512, width=512).images[0]
    image_ov.save(image_path)
    return image_path
