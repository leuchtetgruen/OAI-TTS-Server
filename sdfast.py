import torch
from diffusers import DiffusionPipeline, DDIMScheduler
from huggingface_hub import hf_hub_download
import sys
base_model_id = "runwayml/stable-diffusion-v1-5"
repo_name = "ByteDance/Hyper-SD"
# Take 2-steps lora as an example
ckpt_name = "Hyper-SD15-8steps-lora.safetensors"
# Load model.
#pipe = DiffusionPipeline.from_pretrained(base_model_id, torch_dtype=torch.float16, variant="fp16").to("cuda")
pipe = DiffusionPipeline.from_pretrained(base_model_id, torch_dtype=torch.float32).to("cpu")
pipe.load_lora_weights(hf_hub_download(repo_name, ckpt_name))
pipe.fuse_lora()
# Ensure ddim scheduler timestep spacing set as trailing !!!
pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
prompt= sys.argv[1]
image=pipe(prompt=prompt, num_inference_steps=8, guidance_scale=0).images[0]
image.save('image.png')
