import torch
import datetime
import os
import random

from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video

# load pipeline
pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# optimize for GPU memory
pipe.enable_model_cpu_offload()
pipe.enable_vae_slicing()

def generate_movie_from_text(movie_desc):
    random_image_name = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join([str(random.randint(1,10)) for i in range(5)])
    vedio_path = os.path.join("temp", "movie", random_image_name + ".mp4")
    video_frames = pipe(movie_desc, num_inference_steps=25, num_frames=200).frames
    return export_to_video(video_frames, vedio_path)

if __name__ == '__main__':
    generate_movie_from_text("Spiderman is surfing. Darth Vader is also surfing and following Spiderman")
